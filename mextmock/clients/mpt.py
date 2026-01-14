from collections.abc import Generator
from typing import Any

import httpx
from fastapi import Depends

from mextmock.clients.base import BaseAsyncAPIClient
from mextmock.config import settings
from mextmock.utils import AuthContext, get_auth_context


class MPTClientAuth(httpx.Auth):
    def __init__(self, token: str):
        self.token = token

    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        request.headers["Authorization"] = f"Bearer {self.token}"
        yield request


class MPTAsyncClient(BaseAsyncAPIClient):
    def __init__(self, token: str):
        self._token = token
        super().__init__()

    @property
    def base_url(self):
        return f"{settings.base_url}"

    @property
    def auth(self):
        return MPTClientAuth(self._token)

    async def fetch_order_by_id(
        self,
        order_id: str,
    ) -> dict[str, Any]:
        response = await self.httpx_client.get(f"/commerce/orders/{order_id}?select=agreement,"
                                               f"subscriptions,assets,listing.priceList,"
                                               f"audit,product.settings.splitBilling,"
                                               f"agreement.subscriptions,lines.item,"
                                               f"certificates,lines.price.markupSource,"
                                               f"licensee.eligibility,-agreement.subscriptions,"
                                               f"-agreement.parameters,-agreement.lines")
        response.raise_for_status()
        return response.json()



    async def complete_order(
        self, order_id: str, task_id:str
    ) -> dict[str, Any]:
        response = await self.httpx_client.post(
            f"/commerce/orders/{order_id}/complete",
            json={
                "fulfillment": [
                    {
                        "externalId": "task_id",
                        "value": task_id,
                    }
                ]
            }

        )
        response.raise_for_status()
        return response.json()

    async def fetch_task_by_id(
        self,
        task_id: str,
    ) -> dict[str, Any]:
        response = await self.httpx_client.get(f"/system/tasks/{task_id}")
        response.raise_for_status()
        return response.json()

    async def change_task_status_to_processing(
            self,
            task_id: str,
    ):
        response = await self.httpx_client.post(f"/system/tasks/{task_id}/execute")
        response.raise_for_status()
        return response.json()

    async def reschedule_task(
            self,
            task_id: str,
    ):
        response = await self.httpx_client.post(f"/system/tasks/{task_id}/reschedule")
        response.raise_for_status()
        return response.json()

    async def update_task_progress(self,task_id:str,
                                   progress: float,
                                   installation_id:str,
                                   extension_id:str,
                                   account_id: str):
        response = await self.httpx_client.put(
            f"/system/tasks/{task_id}",
            json={
                "progress": progress,
                "parameters": {
                    "installationId": installation_id,
                    "extensionId": extension_id,
                    "accountId": account_id,
                }
            }
        )
        response.raise_for_status()
        return response.json()
    async def change_task_status_to_complete(
            self,
            task_id: str,
    ):
        response = await self.httpx_client.post(f"/system/tasks/{task_id}/complete")
        response.raise_for_status()
        return response.json()

    async def get_installation_token(
            self,
            installation_id: str,
    ):
        response = await self.httpx_client.post(
            f"/extensibility/installations/{installation_id}/token")
        response.raise_for_status()
        token = response.json()["token"]
        return token


    async def get_subscriptions(
            self,
            order_id: str,
    ):
        response = await self.httpx_client.get(f"/commerce/orders/{order_id}/subscriptions"
                                               f"?select=parameters,agreement,lines,audit")
        response.raise_for_status()
        return response.json()

    async def create_subscription(
            self,
            name:str,
            lines: list[dict[str, Any]],
            vendor_id:str,
            order_id: str,
            parameters: dict[str, Any] | None = None,

    ):
        _lines = []
        for line in lines:
            _lines.append({"id":line["id"]})

        response = await self.httpx_client.post(
            f"/commerce/orders/{order_id}/subscriptions",
            json={
                "name": name,
                "parameters": parameters or {},
                "externalIds": {
                    "vendor": vendor_id,
                },
                "lines": _lines,
            }
        )
        response.raise_for_status()
        return response.json()





def get_service_api_client():
    return MPTAsyncClient(token=settings.api_key)

async def get_installation_api_client(auth_context: AuthContext = Depends(get_auth_context)):
    if auth_context is None:
        return None
    mpt_service_api_client = get_service_api_client()
    vendor_token = await mpt_service_api_client.get_installation_token(auth_context.installation_id)
    return MPTAsyncClient(token=vendor_token)
