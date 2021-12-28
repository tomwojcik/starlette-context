from contextvars import Token
from typing import Optional, Sequence, Union

from starlette.requests import HTTPConnection, Request
from starlette.responses import PlainTextResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from starlette_context import _request_scope_context_storage
from starlette_context.plugins import Plugin
from starlette_context.errors import (
    ConfigurationError,
    StarletteContextClientException,
)


class RawContextMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        plugins: Optional[Sequence[Plugin]] = None,
    ) -> None:
        self.app = app
        for plugin in plugins or ():
            if not isinstance(plugin, Plugin):
                raise ConfigurationError(
                    f"Plugin {plugin} is not a valid instance"
                )

        self.plugins = plugins or ()

    async def set_context(
        self, request: Union[Request, HTTPConnection]
    ) -> dict:
        """
        You might want to override this method.

        The dict it returns will be saved in the scope of a context. You can
        always do that later.
        """
        return {
            plugin.key: await plugin.process_request(request)
            for plugin in self.plugins
        }

    @staticmethod
    def get_request_object(
        scope, receive, send
    ) -> Union[Request, HTTPConnection]:
        # here we instantiate HTTPConnection instead of a Request object
        # because only headers are needed so that's sufficient.
        # If you need the payload etc for your plugin
        # instantiate Request(scope, receive, send)
        return HTTPConnection(scope)

    async def __call__(
        self, scope: Scope, receive: Receive, send: Send
    ) -> None:
        if scope["type"] not in ("http", "websocket"):  # pragma: no cover
            await self.app(scope, receive, send)
            return

        async def send_wrapper(message: Message) -> None:
            for plugin in self.plugins:
                await plugin.enrich_response(message)
            await send(message)

        request = self.get_request_object(scope, receive, send)

        try:
            context = await self.set_context(request)
        except StarletteContextClientException as e:
            # mimics ExceptionMiddleware.http_exception
            resp = PlainTextResponse(e.detail, status_code=e.status_code)

            headers = [
                (k.encode(), v.encode()) for k, v in resp.headers.items()
            ]

            message_head: Message = {
                "type": "http.response.start",
                "status": resp.status_code,
                "headers": headers,
            }

            await send(message_head)

            message_body: Message = {
                "type": "http.response.body",
                "body": resp.body,
                "headers": headers,
            }
            await send(message_body)
            return

        token: Token = _request_scope_context_storage.set(context)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            _request_scope_context_storage.reset(token)
