import datetime
from contextvars import Token
from typing import Optional
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from starlette_context import _request_scope_context_storage, context
from starlette_context.header_contants import HeaderConstants


class BasicContextMiddleware(BaseHTTPMiddleware):
    @staticmethod
    def get_from_header_by_key(request: Request, key: str) -> Optional[str]:
        # http/2 headers lowercase
        if key != key.lower():
            return request.headers.get(key) or request.headers.get(key.lower())
        return request.headers.get(key)

    def get_request_id(self, request: Request) -> str:
        return (
            self.get_from_header_by_key(request, HeaderConstants.rid)
            or uuid4().hex
        )

    def get_correlation_id(self, request: Request) -> str:
        return (
            self.get_from_header_by_key(request, HeaderConstants.cid)
            or uuid4().hex
        )

    def get_user_agent(self, request: Request) -> Optional[str]:
        return self.get_from_header_by_key(request, HeaderConstants.ua)

    @staticmethod
    def rfc1123_to_dt(s: str) -> datetime.datetime:
        return datetime.datetime.strptime(s, "%a, %d %b %Y %H:%M:%S")

    def get_date(self, request: Request) -> Optional[datetime.datetime]:
        """
        Has to be as stated in rfc2616 which uses rfc1123.
        Has to be in GMT.
        Returns UTC datetime.

        Examples allowed:
            Wed, 01 Jan 2020 04:27:12 GMT
            Wed, 01 Jan 2020 04:27:12
        """
        rfc1123 = self.get_from_header_by_key(request, HeaderConstants.date)
        if not rfc1123:
            return

        dt_str, dt_data = rfc1123[:25], rfc1123[25:]

        if dt_data.strip() not in ("", "GMT"):  # I allow to assume GMT
            raise ValueError(
                "Date header in wrong format, has to match rfc1123."
            )

        return self.rfc1123_to_dt(dt_str.strip())

    def get_forwarded_for(self, request: Request) -> Optional[str]:
        return self.get_from_header_by_key(request, HeaderConstants.forwarded_for)

    def set_context(self, request: Request) -> dict:
        return {
            HeaderConstants.cid: self.get_correlation_id(request),
            HeaderConstants.rid: self.get_request_id(request),
            HeaderConstants.date: self.get_date(request),
            HeaderConstants.forwarded_for: self.get_forwarded_for(request),
            HeaderConstants.ua: self.get_user_agent(request),
        }

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        token: Token = _request_scope_context_storage.set(
            self.set_context(request)  # type: ignore
        )
        try:
            response = await call_next(request)
            response.headers[HeaderConstants.cid] = context[
                HeaderConstants.cid
            ]
            response.headers[HeaderConstants.rid] = context[
                HeaderConstants.rid
            ]
        finally:
            _request_scope_context_storage.reset(token)
        return response
