import abc
import uuid
from starlette.requests import HTTPConnection, Request
from starlette.responses import Response
from starlette.types import Message
from typing import Any, Dict, Optional, Union

class Plugin(metaclass=abc.ABCMeta):
    key: str
    async def extract_value_from_header_by_key(
        self, request: Union[Request, HTTPConnection]
    ) -> Optional[Any]: ...
    async def process_request(
        self, request: Union[Request, HTTPConnection]
    ) -> Optional[Any]: ...
    async def enrich_response(self, arg: Union[Response, Message]) -> None: ...

class PluginUUIDBase(Plugin):
    uuid_functions_mapper: Dict[int, uuid.UUID]
    force_new_uuid: bool
    version: int
    validate: bool
    def __init__(
        self,
        force_new_uuid: bool = ...,
        version: int = ...,
        validate: bool = ...,
    ) -> None: ...
    def validate_uuid(self, uuid_to_validate: str) -> None: ...
    def get_new_uuid(self) -> str: ...
    async def extract_value_from_header_by_key(
        self, request: Union[Request, HTTPConnection]
    ) -> Optional[str]: ...
    async def enrich_response(self, arg: Any) -> None: ...
