import json
import logging
from pathlib import Path
import random

import httpx
from devtools import pformat
from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles

from mextmock.config import settings
from mextmock.logging import setup_logging
from mextmock.schemas import Event

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

def platform_api_auth():
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.api_key}"
    }

def platform_api_get(path: str):
    ret = httpx.get(f"{settings.base_url}{path}", headers=platform_api_auth())
    ret.raise_for_status()
    return ret.json()

def platform_api_put(path: str, data: dict):
    ret = httpx.put(f"{settings.base_url}{path}", headers=platform_api_auth(), json=data)
    ret.raise_for_status()
    return ret.json()

def get_order(id: str):
    return platform_api_get(f"/commerce/orders/{id}")

api = APIRouter(prefix="/public/v1")

@api.post(
    "/orders",
    tags=["Event handlers"],
)
async def process_orders(event: Event):
    """
    Subscribe to **Orders** events (*platform.commerce.order*).
    Accept only **Orders** which status is `Processing`.
    """
    logger.info(f"START: event: {event.object.id} status: {event.object.status}")

    order = get_order(event.object.id)
    logger.info(f"Order: {order.id} status: {order.status}")

    if order.status != "Processing":
        logger.info(f"END: order status is not Processing: {order.id} status: {order.status}")
        return {"response": "OK"}

    pphase_extid = 'processing_phase'
    for ffpp in order.parameters.fullfilment:
        if ffpp.externalId == pphase_extid:
            pphase = ffpp.value
            break

    if not ffpp:
        ffpp = {
            "externalId": pphase_extid,
            "value": "0"
        }
        order.parameters.fullfilment.append(ffpp)

    try:
        pphase_int = int(pphase.value)
        pphase_int += 1
        logger.info(f"Incremented {pphase_extid} to {pphase_int}")
    except (ValueError, TypeError):
        logger.info(f"Invalid value of {pphase_extid} in {ffpp}, reset to 1")
        pphase_int = 1

    platform_api_put(f"/commerce/orders/{order.id}", {
        "parameters": {
            "fullfilment": order.parameters.fullfilment
        }
    })

    wait_time = 60 * random.randint(1, 60)
    logger.info(f"sleeping for {wait_time} seconds")

    if pphase_int >= 10:
        logger.info(f"END: {pphase_extid} is reached 10 -> stop processing")
        return {"response": "OK"}

    logger.info(f"END: {pphase_extid} is less than 10 -> continue processing")
    return {"response": "Delay", "delay": wait_time}


app.include_router(api)
