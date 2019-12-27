# it has to be in one file due to the scope of _request_scope_context_storage

from contextvars import ContextVar, Token
from uuid import uuid4

from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request

_request_scope_context_storage: ContextVar[str] = ContextVar(
    "starlette_context"
)


def get_context() -> dict:
    """
    Returns entire dictionary stored for this request.
    """
    return _request_scope_context_storage.get()


def set_context(**kwargs) -> dict:
    """
    Allows you to set custom key: value pair in runtime.
    """
    ctx = get_context()
    ctx.update(kwargs)
    return ctx


class CreateEmptyContextMiddleware(BaseHTTPMiddleware):
    """
    Middleware that creates empty context for request it's used on.
    Otherwise you won't be able to make use of get/set functions.
    """

    def set_context(self, request: Request) -> dict:
        """
        You might want to override this method.
        The dict it returns will be saved in scope.
        You can always to that later.
        Empty context will be instantiated anyway.
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


class PreserveCustomContextMiddleware(CreateEmptyContextMiddleware):
    cid = "X-Correlation-ID"
    rid = "X-Request-ID"
    date = "Date"
    forwarded_for = "X-Forwarded-For"
    ua = "User-Agent"

    @staticmethod
    def get_uuid() -> str:
        return uuid4().hex

    @staticmethod
    def get_from_header_by_key(request: Request, key: str):
        return request.headers.get(key)

    def get_request_id(self, request: Request) -> str:
        return (
            self.get_from_header_by_key(request, self.rid) or self.get_uuid()
        )

    def get_correlation_id(self, request: Request) -> str:
        return (
            self.get_from_header_by_key(request, self.cid) or self.get_uuid()
        )

    def get_user_agent(self, request: Request) -> str:
        return self.get_from_header_by_key(request, self.ua) or None

    def get_date(self, request: Request) -> str:
        return self.get_from_header_by_key(request, self.date) or None

    def get_forwarded_for(self, request: Request) -> str:
        return self.get_from_header_by_key(request, self.forwarded_for) or None

    def set_context(self, request) -> dict:
        return {
            self.cid: self.get_correlation_id(request),
            self.rid: self.get_request_id(request),
            self.date: self.get_date(request),
            self.forwarded_for: self.get_forwarded_for(request),
            self.ua: self.get_user_agent(request),
        }
