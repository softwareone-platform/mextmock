from abc import ABC, abstractmethod
from functools import cached_property

import httpx
from httpx_retries import Retry, RetryTransport

NOT_IMPLEMENTED_ERROR="base_url property must be implemented in subclasses"


class BaseAsyncAPIClient(ABC):

    def __init__(self, limit: int = 50):
        self.limit = limit

    @property
    @abstractmethod
    def base_url(self):
        raise NotImplementedError(NOT_IMPLEMENTED_ERROR)

    @property
    @abstractmethod
    def auth(self):
        raise NotImplementedError(NOT_IMPLEMENTED_ERROR)

    @cached_property
    def httpx_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            base_url=self.base_url,
            auth=self.auth,
            timeout=httpx.Timeout(connect=5.0, read=180.0, write=5.0, pool=5.0),
            transport=RetryTransport(retry=Retry(total=5, backoff_factor=0.5)),
        )


    async def close(self):
        await self.httpx_client.aclose()
