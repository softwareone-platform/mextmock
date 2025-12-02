import logging
from pathlib import Path
from typing import Annotated

from devtools import pformat
from fastapi import APIRouter, FastAPI, Depends, Header
from fastapi.staticfiles import StaticFiles

from mextmock.clients.mpt import MPTAsyncClient, get_service_api_client, get_vendor_api_client
from mextmock.logging import setup_logging
from mextmock.schemas import Event
from mextmock.utils import get_auth_context, AuthContext, process_order_parameters

logger = logging.getLogger("mextmock")
setup_logging()

app = FastAPI(
    title="SWO Marketplace Extension Mock",
    description="API to orchestrate OpenZiti for Extensions.",
    swagger_ui_parameters={"showExtensions": False, "showCommonExtensions": False},
    openapi_tags=[
        {
            "name": "Event handlers",
            "description": "Endpoints for receiving platform events.",
        },
    ],
    version="5.0.0",
    openapi_url="/public/v1/openapi.json",
    docs_url="/public/v1/docs",
    redoc_url="/public/v1/redoc",
)

app.mount(
    "/static",
    StaticFiles(
        directory=Path(__file__).parent.resolve() / "static",
        html=True,
    ),
    name="static",
)

api = APIRouter(prefix="/public/v1")

@api.post(
    "/orders",
    tags=["Event handlers"],
)
async def process_orders(event: Event,
                         auth_context: AuthContext | None = Depends(get_auth_context),
                         mpt_api_client: MPTAsyncClient = Depends(get_service_api_client),
                         vendor_api_client: MPTAsyncClient = Depends(get_vendor_api_client)

                         ):
    """
    Subscribe to **Orders** events (*platform.commerce.order*).
    Accept only **Orders** which status is `Processing`.
    """
    logger.info(f"auth context: {auth_context}")
    logger.info(
        f"New event received: {pformat(event)}"
    )
    task_id = event.task.id
    order_id = event.object.id
    order_details = await mpt_api_client.fetch_order_by_id(order_id=order_id)
    ordering_external_id, ordering_value = process_order_parameters(order_details)
    logger.info(f"ordering external_id: {ordering_external_id}")
    logger.info(f"ordering value: {ordering_value}")
    if ordering_external_id == "scenario":
        #chage the task's status to executing
        logger.info(f"changing task {task_id} status to Executing")
        await vendor_api_client.change_task_status_to_execute(task_id=task_id)
        # chane the task's status to complete
        logger.info(f"changing task {task_id} status to Completed")
        await vendor_api_client.change_task_status_to_complete(task_id=task_id)
        # change the order's status to complete
        logger.info(f"changing order {order_id} status to Completed")
        await mpt_api_client.complete_order(order_id=order_id, task_id=task_id)
        return {"response": "OK"}
    else:
        return {"response": "ERROR"}
app.include_router(api)
