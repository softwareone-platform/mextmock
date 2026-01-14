import logging
from pathlib import Path

from devtools import pformat
from fastapi import APIRouter, Depends, FastAPI
from fastapi.staticfiles import StaticFiles

from mextmock.logging_config import setup_logging
from mextmock.scenarios.processor import BaseScenarioProcessor, get_scenario_process
from mextmock.schemas import Event
from mextmock.utils import AuthContext, get_auth_context

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
                         order_processor: BaseScenarioProcessor = Depends(get_scenario_process),

                         ):
    """
    Subscribe to **Orders** events (*platform.commerce.order*).
    Accept only **Orders** which status is `Processing`.
    """
    logger.info(f"auth context: {auth_context}")
    logger.info(
        f"New event received: {pformat(event)}"
    )

    return await order_processor.process_order(event,auth_context)

app.include_router(api)
