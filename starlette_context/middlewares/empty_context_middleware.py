from _contextvars import Token

from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette_context import _request_scope_context_storage


class EmptyContextMiddleware(BaseHTTPMiddleware):
    """
    Middleware that creates empty context for request it's used on.
    If not used, you won't be able to use context object.
    """

    def set_context(self, request: Request) -> dict:
        """
        You might want to override this method.
        The dict it returns will be saved in the scope of a context.
        You can always do that later.
        """
        return {}

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ):
        token: Token = _request_scope_context_storage.set(
            self.set_context(request)
        )  # noqa
        try:
            response = await call_next(request)
        finally:
            _request_scope_context_storage.reset(token)
        return response
