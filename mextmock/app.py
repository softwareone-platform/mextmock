import logging

from devtools import pformat
from fastapi import FastAPI

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
    root_path="/public/v1",
)



@app.post(
    "/orders",
    tags=["Event handlers"],
)
async def process_orders(event: Event):
    """
    Subscribe to **Orders** events (*platform.commerce.order*).
    Accept only **Orders** which status is `Processing`.
    """
    logger.info(
        f"New event received: {pformat(event)}"
    )
    return {"response": "OK"}
