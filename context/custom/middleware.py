from contextvars import ContextVar, Token
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

_request_scope_context_storage: ContextVar[str] = ContextVar(
    "PreserveCustomContextMiddleware"
)


def get_context() -> dict:
    """
    Returns entire custom dictionary stored for this request.
    """
    return _request_scope_context_storage.get()


def update_context(**kwargs) -> dict:
    """
    Allows you to set custom key: value pair in runtime, after the creation of user 'context'.
    """
    ctx = get_context()
    ctx.update(kwargs)
    return ctx


class PreserveCustomContextMiddleware(BaseHTTPMiddleware):
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
        return self.get_from_header_by_key(request, self.cid) or self.get_uuid()

    def get_correlation_id(self, request: Request) -> str:
        return self.get_from_header_by_key(request, self.cid) or self.get_uuid()

    def get_user_agent(self, request: Request) -> str:
        return self.get_from_header_by_key(request, self.ua) or self.get_uuid()

    def get_date(self, request: Request) -> str:
        return self.get_from_header_by_key(request, self.date) or self.get_uuid()

    def get_forwarded_for(self, request: Request) -> str:
        return (
            self.get_from_header_by_key(request, self.forwarded_for) or self.get_uuid()
        )

    def set_context(self, request: Request) -> dict:
        """
        You might want to override this method if you want to pass some data from request.
        You may always use update_context function, but it will require you to run get on contextvar,
        which will result in worse performance, event with O(1).
        """
        return {}

    def set_response_headers(self, response: Response):
        """
        Here you might want to set cid and rid to headers like
        response.headers[self.cid] = self.get_correlation_id(request)
        response.headers[self.rid] = self.get_request_id(request)
        """
        return response

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        token: Token = _request_scope_context_storage.set(
            self.set_context(request)
        )  # noqa
        try:
            response = await call_next(request)
        finally:
            _request_scope_context_storage.reset(token)

        self.set_response_headers(response)
        return response
