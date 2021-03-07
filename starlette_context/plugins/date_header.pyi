import datetime
from starlette.requests import HTTPConnection, Request
from starlette_context.plugins.base import Plugin
from typing import Optional, Union

class DateHeaderPlugin(Plugin):
    key: str
    @staticmethod
    def rfc1123_to_dt(s: str) -> datetime.datetime: ...
    async def process_request(
        self, request: Union[Request, HTTPConnection]
    ) -> Optional[datetime.datetime]: ...
