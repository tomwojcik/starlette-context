import abc
import uuid
from typing import Any, Optional, Union

from starlette.datastructures import MutableHeaders
from starlette.requests import HTTPConnection, Request
from starlette.responses import Response
from starlette.types import Message

from starlette_context import context

__all__ = ["Plugin", "PluginUUIDBase"]


class Plugin(metaclass=abc.ABCMeta):
    """
    Base class for building those plugins to extract things from request.
    One plugins should be responsible for extracting one thing.
    key: the key that allows to access value in headers
    """

    key: str

    async def extract_value_from_header_by_key(
        self, request: Union[Request, HTTPConnection]
    ) -> Optional[Any]:
        return request.headers.get(self.key)

    async def process_request(
        self, request: Union[Request, HTTPConnection]
    ) -> Optional[Any]:
        """
        Runs always on request.
        Extracts value from header by default.
        """
        assert isinstance(self.key, str)
        return await self.extract_value_from_header_by_key(request)

    async def enrich_response(self, arg: Union[Response, Message]) -> None:
        """
        Runs always on response.
        Does nothing by default.
        """
        ...


class PluginUUIDBase(Plugin):
    uuid_functions_mapper = {4: uuid.uuid4}

    def __init__(
        self,
        force_new_uuid: bool = False,
        version: int = 4,
        validate: bool = True,
    ):
        if version not in self.uuid_functions_mapper:
            raise TypeError(f"UUID version {version} is not supported.")
        self.force_new_uuid = force_new_uuid
        self.version = version
        self.validate = validate

    def validate_uuid(self, uuid_to_validate: str) -> None:
        try:
            uuid.UUID(uuid_to_validate, version=self.version)
        except Exception as e:
            raise ValueError("Wrong uuid") from e

    def get_new_uuid(self) -> str:
        func = self.uuid_functions_mapper[self.version]
        return func().hex

    async def extract_value_from_header_by_key(
        self, request: Union[Request, HTTPConnection]
    ) -> Optional[str]:

        value = await super().extract_value_from_header_by_key(request)

        # if force_new_uuid or correlation id was not found, create one
        if self.force_new_uuid or not value:
            value = self.get_new_uuid()

        if self.validate:
            self.validate_uuid(value)

        return value

    async def enrich_response(self, arg) -> None:
        value = str(context.get(self.key))

        # for ContextMiddleware
        if isinstance(arg, Response):
            arg.headers[self.key] = value
        # for ContextPureMiddleware
        else:
            if arg["type"] == "http.response.start":
                headers = MutableHeaders(scope=arg)
                headers.append(self.key, value)
