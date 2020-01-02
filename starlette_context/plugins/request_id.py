import uuid
from typing import Optional

from starlette.requests import Request

from starlette_context.header_keys import HeaderKeys
from starlette_context.plugins.plugin import Plugin


class RequestIdPlugin(Plugin):
    key = HeaderKeys.request_id
    add_to_response = True

    def get_from_header_by_key(self, request: Request) -> Optional[str]:
        super(RequestIdPlugin, self).get_from_header_by_key(request)
        if self.value is None:
            self.value = uuid.uuid4().hex
        return self.value
