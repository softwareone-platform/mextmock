import asyncio
import logging
import random
from abc import ABC, abstractmethod
from enum import Enum

from fastapi import Depends

from mextmock.clients.mpt import MPTAsyncClient, get_installation_api_client, get_service_api_client
from mextmock.config import settings
from mextmock.schemas import Event
from mextmock.utils import get_ordering_parameter

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    Queued = "Queued"
    Processing = "Processing"
    Succeed = "Completed"
    Rescheduled = "Rescheduled"
    Failed = "Failed"
    Blocked = "Blocked"
    Canceled = "Canceled"


class BaseScenarioProcessor(ABC):
    def __init__(
        self, mpt_api_client: MPTAsyncClient, vendor_api_client: MPTAsyncClient, order_details: dict
    ):
        self.mpt_api_client = mpt_api_client
        self.vendor_api_client = vendor_api_client
        self.order_details = order_details
        self.background_tasks: set[asyncio.Task] = set()

    @abstractmethod
    async def process_order(self, event, auth_context): ...

    async def complete_order(self, account_id: str, order_id: str, task_id: str):
        # get order's subscriptions
        subscriptions = await self.mpt_api_client.get_subscriptions(order_id=order_id)
        if len(subscriptions["data"]) == 0:
            # no subscriptions for this order. Need to create it
            logger.info(
                "no subscriptions found for order %s. Going to create a new subscription"
            ,order_id)
            await self.mpt_api_client.create_subscription(
                name="Subscription test",
                lines=self.order_details["lines"],
                vendor_id=account_id,
                order_id=order_id,
            )
        # change the order's status to complete
        logger.info("Complete the order %s", order_id)
        return await self.mpt_api_client.complete_order(order_id=order_id, task_id=task_id)


class RescheduleScenario(BaseScenarioProcessor):
    async def process_order(self, event, auth_context):
        logger.info("Processing SimpleRescheduleScenario")
        task_id = event.task.id
        order_id = event.object.id
        task_detail = await self.mpt_api_client.fetch_task_by_id(task_id=task_id)
        task_status = task_detail["status"]
        current_task_progress = task_detail["progress"]
        logger.info(
            "Task %s status=%s progress=%s%%",
            task_id,
            task_status,
            current_task_progress,
        )

        def create_background_task(coro):
            task = asyncio.create_task(coro)
            self.background_tasks.add(task)
            task.add_done_callback(self.background_tasks.discard)
            return task

        async def set_processing_status():
            logger.info("Setting task %s status to Processing", task_id)
            await self.mpt_api_client.change_task_status_to_processing(task_id=task_id)

        async def set_reschedule_status():
            logger.info("Rescheduling task %s", task_id)
            await self.mpt_api_client.reschedule_task(task_id=task_id)

        if task_status == TaskStatus.Queued.value:
            await set_processing_status()
            await self.apply_progress_to_task(event, auth_context, task_detail)
            await set_reschedule_status()

        elif task_status == TaskStatus.Rescheduled.value:
            await set_processing_status()

            if current_task_progress < 100:
                await self.apply_progress_to_task(event, auth_context, task_detail)
                await set_reschedule_status()

            else:
                # complete the order
                logger.info("Completing order %s for task %s", order_id, task_id)
                create_background_task(
                    self.complete_order(
                        account_id=auth_context.account_id,
                        order_id=event.object.id,
                        task_id=task_id,
                    )
                )
                # complete the task
                logger.info("Completing task %s",task_id)
                create_background_task(
                    self.mpt_api_client.change_task_status_to_complete(task_id=task_id)
                )
                return {"response": "OK"}
        return {"response": "Delay", "delay": settings.delay_interval_in_sec}

    async def apply_progress_to_task(self, event, auth_context, task_detail):
        task_id = event.task.id
        current_task_progress = task_detail["progress"]
        random_process = random.randint(1, 100 - current_task_progress)
        new_progress = current_task_progress + random_process
        logger.info("Task %s - Updating progress from %s%% to %s%%", task_id, current_task_progress, new_progress)
        await self.mpt_api_client.update_task_progress(
            task_id=task_id,
            progress=new_progress,
            installation_id=auth_context.installation_id,
            extension_id=auth_context.extension_id,
            account_id=auth_context.account_id,
        )

    async def complete_task(self, task_id):
        return await self.mpt_api_client.change_task_status_to_complete(task_id=task_id)


class ImmediateFailureScenario(BaseScenarioProcessor):

    async def process_order(self, event, auth_context):
        logger.info("Processing ImmediateFailureScenario")
        return {"response": "Cancel"}


class SimpleFulfillmentScenario(BaseScenarioProcessor):
    async def process_order(self, event, auth_context):
        logger.info("Processing SimpleFulfillmentScenario")
        task_id = event.task.id
        order_id = event.object.id
        # change the task's status to executing
        logger.info("Changing task %s status to Processing",task_id)
        await self.mpt_api_client.change_task_status_to_processing(task_id=task_id)
        # change the task's progress to 100
        logger.info("Updating %s progress to 100%%",task_id)
        await self.mpt_api_client.update_task_progress(
            task_id=task_id,
            progress=100,
            installation_id=auth_context.installation_id,
            extension_id=auth_context.extension_id,
            account_id=auth_context.account_id,
        )
        # change the task's status to complete
        logger.info("Changing task %s status to Completed",task_id)
        await self.complete_order(
            account_id=auth_context.account_id, order_id=order_id, task_id=task_id
        )
        await self.mpt_api_client.change_task_status_to_complete(task_id=task_id)
        return {"response": "OK"}


async def get_scenario_process(
    event: Event,
    mpt_api_client: MPTAsyncClient = Depends(get_service_api_client),
    installation_api_client: MPTAsyncClient = Depends(get_installation_api_client),
):
    scenario_map = {
        "simple" : SimpleFulfillmentScenario,
        "immediate_failure" : ImmediateFailureScenario,
        "simple_reschedule": RescheduleScenario,
    }
    order_id = event.object.id
    order_details = await mpt_api_client.fetch_order_by_id(order_id=event.object.id)
    scenario_parm = get_ordering_parameter(order_details, "scenario")
    logger.info("Order Scenario: %s", scenario_parm)
    if not scenario_parm or "value" not in scenario_parm:
        raise ValueError("Missing scenario parameter for order %s", order_id)
    scenario_value = scenario_parm["value"]
    scenario_cls = scenario_map[scenario_value]
    if not scenario_cls:
        raise ValueError("Unsupported scenario parameter for order %s", order_id)
    return scenario_cls(mpt_api_client, installation_api_client, order_details)
