import abc
import uuid
from typing import Union, Optional

from starlette.requests import Request, HTTPConnection

__all__ = [
    "ProcessRequestStrategy",
    "BasicProcessRequestStrategy",
    "UUIDProcessRequestStrategy",
]


class ProcessRequestStrategy(metaclass=abc.ABCMeta):
    def __init__(self, key):
        self.key = key

    async def extract_value_from_header_by_key(
        self, request: Union[Request, HTTPConnection]
    ) -> Optional[Union[str, int, dict]]:
        return request.headers.get(self.key)

    @abc.abstractmethod
    async def process_request(
        self, request: Union[Request, HTTPConnection]
    ) -> Union[str, int, dict]:
        ...


class BasicProcessRequestStrategy(ProcessRequestStrategy):
    async def process_request(
        self, request: Union[Request, HTTPConnection]
    ) -> Union[str, int, dict]:
        return await self.extract_value_from_header_by_key(self.key)


class UUIDProcessRequestStrategy(ProcessRequestStrategy):
    uuid_functions_mapper = {4: uuid.uuid4}

    def __init__(
        self,
        force_new_uuid: bool = False,
        version: int = 4,
        validate: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)
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

    async def process_request(
        self, request: Union[Request, HTTPConnection]
    ) -> Union[str, int, dict]:
        value = await self.extract_value_from_header_by_key(request)

        # if force_new_uuid or correlation id was not found, create one
        if self.force_new_uuid or not value:
            value = self.get_new_uuid()

        if self.validate:
            self.validate_uuid(value)

        return value
