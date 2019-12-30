from _contextvars import Token
from uuid import uuid4

from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette_context import _request_scope_context_storage, context


class BasicContextMiddleware(BaseHTTPMiddleware):
    cid = "X-Correlation-ID"
    rid = "X-Request-ID"
    date = "Date"
    forwarded_for = "X-Forwarded-For"
    ua = "User-Agent"

    def __init__(self, *args, **kwargs):
        super(BasicContextMiddleware, self).__init__(*args, **kwargs)

    @staticmethod
    def get_from_header_by_key(request: Request, key: str):
        # http/2 headers lowercase
        if key != key.lower():
            return request.headers.get(key) or request.headers.get(key.lower())
        return request.headers.get(key)

    def get_request_id(self, request: Request) -> str:
        return self.get_from_header_by_key(request, self.rid) or uuid4().hex

    def get_correlation_id(self, request: Request) -> str:
        return self.get_from_header_by_key(request, self.cid) or uuid4().hex

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

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ):
        token: Token = _request_scope_context_storage.set(
            self.set_context(request)
        )  # noqa
        try:
            response = await call_next(request)
            response.headers[self.cid] = context[self.cid]
            response.headers[self.rid] = context[self.rid]
        finally:
            _request_scope_context_storage.reset(token)
        return response
