import uuid
from typing import Optional

from starlette.requests import Request
from starlette.responses import Response

from starlette_context.plugins.plugin import Plugin


class PluginUUIDBase(Plugin):
    uuid_functions_mapper = {4: uuid.uuid4}

    def __init__(self, force_new_uuid: bool = False, version: int = 4):
        super().__init__()
        if version not in self.uuid_functions_mapper:
            raise TypeError(f"UUID version {version} is not supported.")
        self.force_new_uuid = force_new_uuid
        self.version = version

    def validate_uuid(self, uuid_to_validate: str) -> None:
        try:
            uuid.UUID(uuid_to_validate, version=self.version)
        except Exception as e:
            raise ValueError("Wrong uuid") from e

    def get_new_uuid(self) -> str:
        func = self.uuid_functions_mapper[self.version]
        return func().hex

    async def extract_value_from_header_by_key(
        self, request: Request
    ) -> Optional[str]:
        if not self.force_new_uuid:
            await super().extract_value_from_header_by_key(request)

        if self.value is None:
            self.value = self.get_new_uuid()

        self.validate_uuid(self.value)

        return self.value

    async def enrich_response(self, response: Response) -> None:
        await self._add_kv_to_response_headers(response)
