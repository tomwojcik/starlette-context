import uuid
from typing import Optional

from starlette.requests import Request
from starlette.responses import Response

from starlette_context.header_keys import HeaderKeys
from starlette_context.plugins.plugin import Plugin


class CorrelationIdPlugin(Plugin):
    key = HeaderKeys.correlation_id

    async def extract_value_from_header_by_key(
        self, request: Request
    ) -> Optional[str]:
        await super(
            CorrelationIdPlugin, self
        ).extract_value_from_header_by_key(request)
        if self.value is None:
            self.value = uuid.uuid4().hex
        return self.value

    async def enrich_response(self, response: Response) -> None:
        await self._add_kv_to_response_headers(response)
