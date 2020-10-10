from contextvars import Token
from typing import Optional, Sequence, Union

from starlette.requests import HTTPConnection, Request
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from starlette_context import _request_scope_context_storage
from starlette_context.plugins import Plugin


class RawContextMiddleware:
    def __init__(
        self, app: ASGIApp, plugins: Optional[Sequence[Plugin]] = None
    ) -> None:
        self.app = app
        self.plugins = plugins or ()
        if not all([isinstance(plugin, Plugin) for plugin in self.plugins]):
            raise TypeError("This is not a valid instance of a plugin")

    async def set_context(
        self, request: Union[Request, HTTPConnection]
    ) -> dict:
        """
        You might want to override this method.
        The dict it returns will be saved in the scope of a context.
        You can always do that later.
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

        _starlette_context_token: Token = _request_scope_context_storage.set(
            await self.set_context(request)
        )

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            _request_scope_context_storage.reset(_starlette_context_token)
