from contextvars import Token
from typing import Optional, Sequence

from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import Response

from starlette_context import _request_scope_context_storage
from starlette_context.middleware.mixin import StarletteContextMiddlewareMixin
from starlette_context.plugins import Plugin
from starlette_context.errors import (
    ConfigurationError,
    StarletteContextException,
)


class ContextMiddleware(BaseHTTPMiddleware, StarletteContextMiddlewareMixin):
    """
    Middleware that creates empty context for request it's used on. If not
    used, you won't be able to use context object.

    Not to be used with StreamingResponse / FileResponse.
    https://github.com/encode/starlette/issues/1012#issuecomment-673461832
    """

    def __init__(
        self,
        plugins: Optional[Sequence[Plugin]] = None,
        **kwargs,
    ) -> None:
        BaseHTTPMiddleware.__init__(
            self, app=kwargs["app"], dispatch=kwargs.get("dispatch")
        )
        StarletteContextMiddlewareMixin.__init__(self, **kwargs)
        for plugin in plugins or ():
            if not isinstance(plugin, Plugin):
                raise ConfigurationError(
                    f"Plugin {plugin} is not a valid instance"
                )
        self.plugins = plugins or ()

    async def set_context(self, request: Request) -> dict:
        """
        You might want to override this method.

        The dict it returns will be saved in the scope of a context. You can
        always do that later.
        """
        return {
            plugin.key: await plugin.process_request(request)
            for plugin in self.plugins
        }

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            context = await self.set_context(request)
            token: Token = _request_scope_context_storage.set(context)

            try:
                response = await call_next(request)
                for plugin in self.plugins:
                    await plugin.enrich_response(response)
            finally:
                _request_scope_context_storage.reset(token)

        except StarletteContextException as e:
            response = await self.create_response_from_exception(request, e)

        return response
