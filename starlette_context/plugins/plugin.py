import abc
from typing import Optional, Union

from starlette.requests import Request
from starlette.responses import Response


class Plugin(metaclass=abc.ABCMeta):
    """
    Base class for building those plugins to extract things from request.
    One plugins should be responsible for extracting one thing.

    key: the key that allows to access value in headers
    """
    key: str = None

    def __init__(self):
        self.value = None

    async def extract_value_from_header_by_key(self, request: Request) -> Optional[str]:
        # http/2 headers lowercase
        if self.key != self.key.lower():
            self.value = request.headers.get(self.key) or request.headers.get(
                self.key.lower()
            )
        else:
            self.value = request.headers.get(self.key)

        return self.value

    async def process_request(self, request: Request) -> Union[str, int]:
        assert isinstance(self.key, str)
        return await self.extract_value_from_header_by_key(request)

    async def _add_kv_to_response_headers(self, response: Response) -> None:
        response.headers[self.key] = str(self.value)

    async def enrich_response(self, response: Response) -> None:
        ...
