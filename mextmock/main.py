import json
import logging
from pathlib import Path
from urllib import request

from mrok.agent import ziticorn

import mextmock
from mextmock.config import settings
from mextmock.logging import setup_logging
from mextmock.utils import get_instance_external_id

logger = logging.getLogger("mextmock")
IDENTITY_FILE = Path.cwd() / "identity.json"


def bootstrap():
    setup_logging()

    if not settings.extension_id:
        raise Exception("No Extension ID has been provided.")
    if not settings.base_url:
        raise Exception("No Marketplace API Url has been provided.")
    if not settings.api_key:
        raise Exception("No Marketplace Vendor API Key has been provided.")


    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {settings.api_key}"}

    external_id = get_instance_external_id()

    logger.info(
        f"Boostrap instance for extension {settings.extension_id}: externalId={external_id}",
    )

    data = {
        "externalId": external_id,
        "version": mextmock.__version__,
        "meta": {
            "version": mextmock.__version__,
            "placeholders": [
            ],
            "openapi": "/public/v1/openapi.json",
            "events": [
                {
                    "event": "platform.commerce.order",
                    "filter": "eq(status,Processing)",
                    "path": "/public/v1/orders",
                    "task": True,
                }
            ],
            "plugs": [
                {
                    "id": "subs-actions",
                    "name": "Subscriptions Actions Demo",
                    "description": "Check sockets",
                    "icon": "adobe.png",
                    "socket": "portal.commerce.subscriptions.actions",
                    "href": "/static/index.js"
                },
                {
                   "id": "subs-lines-actions",
                   "name": "Subscriptions Lines Actions Demo",
                   "description": "Check sockets",
                   "icon": "adobe.png",
                   "socket": "portal.commerce.subscriptions.line.actions",
                   "href": "/static/index.js"
                },
                {
                    "id": "sub-tabs",
                    "name": "Subscription Tab Demo",
                    "description": "Check sockets",
                    "icon": "adobe.png",
                    "socket": "portal.commerce.subscriptions.subscription",
                    "href": "/static/index.js"
                },
                {
                    "id": "sub-actions",
                    "name": "Subscription Actions Demo",
                    "description": "Check sockets",
                    "icon": "adobe.png",
                    "socket": "portal.commerce.subscriptions.subscription.actions",
                    "href": "/static/index.js"
                },

                {
                    "id": "agrs-actions",
                    "name": "Agreements Actions Demo",
                    "description": "Check sockets",
                    "icon": "adobe.png",
                    "socket": "portal.commerce.agreements.actions",
                    "href": "/static/index.js"
                },
                {
                   "id": "agrs-lines-actions",
                   "name": "Agreements Lines Actions Demo",
                   "description": "Check sockets",
                   "icon": "adobe.png",
                   "socket": "portal.commerce.agreements.line.actions",
                   "href": "/static/index.js"
                },
                {
                    "id": "agr-tabs",
                    "name": "Agreement Tab Demo",
                    "description": "Check sockets",
                    "icon": "adobe.png",
                    "socket": "portal.commerce.agreements.agreement",
                    "href": "/static/index.js"
                },
                {
                    "id": "agr-actions",
                    "name": "Agreement Actions Demo",
                    "description": "Check sockets",
                    "icon": "adobe.png",
                    "socket": "portal.commerce.agreements.agreement.actions",
                    "href": "/static/index.js"
                },

                {
                     "id": "ords-actions",
                     "name": "Orders Actions Demo",
                     "description": "Check sockets",
                     "icon": "adobe.png",
                     "socket": "portal.commerce.orders.actions",
                     "href": "/static/index.js"
                },
                {
                    "id": "ords-lines-actions",
                    "name": "Orders Lines Actions Demo",
                    "description": "Check sockets",
                    "icon": "adobe.png",
                    "socket": "portal.commerce.orders.line.actions",
                    "href": "/static/index.js"
                },
                {
                     "id": "ord-tabs",
                     "name": "Order Tab Demo",
                     "description": "Check sockets",
                     "icon": "adobe.png",
                     "socket": "portal.standalone.ffc.admin",
                     "href": "/static/index.js"
                },
                {
                     "id": "ord-actions",
                     "name": "Order Actions Demo",
                     "description": "Check sockets",
                     "icon": "adobe.png",
                     "socket": "portal.commerce.orders.order.actions",
                     "href": "/static/index.js"
                },

                {
                  "id": "asts-actions",
                  "name": "Assets Actions Demo",
                  "description": "Check sockets",
                  "icon": "adobe.png",
                  "socket": "portal.commerce.assets.actions",
                  "href": "/static/index.js"
                },
                {
                 "id": "asts-lines-actions",
                 "name": "Assets Lines Actions Demo",
                 "description": "Check sockets",
                 "icon": "adobe.png",
                 "socket": "portal.commerce.assets.line.actions",
                 "href": "/static/index.js"
                },
                {
                  "id": "ast-tabs",
                  "name": "Asset Tab Demo",
                  "description": "Check sockets",
                  "icon": "adobe.png",
                  "socket": "portal.commerce.assets.asset",
                  "href": "/static/index.js"
                },
                {
                  "id": "ast-actions",
                  "name": "Asset Actions Demo",
                  "description": "Check sockets",
                  "icon": "adobe.png",
                  "socket": "portal.commerce.assets.asset.actions",
                  "href": "/static/index.js"
                },
                {
                    "id": "modal",
                    "name": "Just a modal",
                    "description": "Check sockets",
                    "icon": "adobe.png",
                    "href": "/static/index.js"
                }
            ]
        },
    }
    for evtinfo in data["meta"]["events"]:
        msg = (
            f"Register event subscription to {evtinfo['event']} "
            f"(task={evtinfo['task']}, filter={evtinfo.get("filter", "-")}) "
            f"-> {evtinfo["path"]}"
        )
        logger.info(msg)

    if not IDENTITY_FILE.exists():
        logger.info(
            f"Request new identity for {settings.extension_id}: externalId={external_id}",
        )
        data["channel"] = {}
    else:
        identity = json.load(open(IDENTITY_FILE))
        identity_extension = identity.get("mrok", {}).get("extension", "")
        if identity_extension.lower() != settings.extension_id.lower():
            logger.warning(
                f"The existing identity belongs to the extension {identity_extension}. "
                f"Request new identity for {settings.extension_id}: externalId={external_id}",
            )
            data["channel"] = {}

    req = request.Request(
        f"{settings.base_url}/extensibility/extensions/{settings.extension_id}/instances",
        method="POST",
        headers=headers,
        data=json.dumps(data).encode("utf-8"),
    )

    with request.urlopen(req) as res:
        response_data = json.load(res)
        identity = response_data.get("channel", {}).get("identity")
        if identity:
            logger.info(f"Save instance identity to {IDENTITY_FILE}")
            with open(IDENTITY_FILE, "w") as writer:
                json.dump(identity, writer)
        logger.info(
            f"Instance bootstrap for extension {settings.extension_id} completed: "
            f"{response_data["id"]}")


    ziticorn.run("mextmock.app:app", str(IDENTITY_FILE), server_workers=4)


if __name__ == "__main__":
    bootstrap()
