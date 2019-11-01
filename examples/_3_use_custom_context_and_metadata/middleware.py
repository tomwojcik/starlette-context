from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from context.custom.middleware import (
    update_context,
    PreserveCustomContextMiddleware,
)


class CustomContextUsingFunctionFromMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        update_context(data_from="custom_context")
        return await call_next(request)


class CustomContextUsingInheritance(PreserveCustomContextMiddleware):
    def set_context(self, request: Request) -> dict:
        return {
            "correlation_id": self.get_correlation_id(request),
            "request_id": self.get_request_id(request),
        }
