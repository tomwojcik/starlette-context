import abc
from typing import Optional, Union

from starlette.requests import Request
from starlette.responses import Response

from starlette_context import context


class Plugin(metaclass=abc.ABCMeta):
    """
    Base class for building those plugins to extract things from request.
    One plugins should be responsible for extracting one thing.

    key: the key that allows to access value in headers
    """

    key: str = None

    async def extract_value_from_header_by_key(
        self, request: Request
    ) -> Optional[str]:
        """
        Helper method.
        """
        # http/2 headers lowercase
        if self.key != self.key.lower():
            value = request.headers.get(self.key) or request.headers.get(
                self.key.lower()
            )
        else:
            value = request.headers.get(self.key)

        return value

    async def process_request(self, request: Request) -> Union[str, int, dict]:
        """
        Runs always on request.
        Extracts value from header by default.
        """
        assert isinstance(self.key, str)
        return await self.extract_value_from_header_by_key(request)

    async def _add_kv_to_response_headers(self, response: Response) -> None:
        """
        Helper method
        """
        value = context.get(self.key)
        if not isinstance(value, (str, int)):
            raise TypeError(
                "String or int needed. Header value shouldn't be a complex type."  # noqa: E501
            )
        response.headers[self.key] = value

    async def enrich_response(self, response: Response) -> None:
        """
        Runs always on response.
        Does nothing by default.
        """
        ...
