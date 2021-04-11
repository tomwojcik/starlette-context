from starlette.requests import HTTPConnection, Request as Request
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette_context.plugins import Plugin
from typing import Optional, Sequence, Union

class RawContextMiddleware:
    app: ASGIApp
    plugins: Optional[Sequence[Plugin]]
    def __init__(
        self, app: ASGIApp, plugins: Optional[Sequence[Plugin]] = ...
    ) -> None: ...
    async def set_context(
        self, request: Union[Request, HTTPConnection]
    ) -> dict: ...
    @staticmethod
    def get_request_object(
        scope: Scope, receive: Receive, send: Send
    ) -> Union[Request, HTTPConnection]: ...
    async def __call__(
        self, scope: Scope, receive: Receive, send: Send
    ) -> None: ...
