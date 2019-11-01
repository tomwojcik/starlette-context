from uuid import uuid4

from requests import Request, Response
from starlette.middleware.base import RequestResponseEndpoint, BaseHTTPMiddleware

from context.custom.middleware import (
    PreserveCustomContextMiddleware,
    update_context,
)


class SetRequestAndCorrelationIdInContext(PreserveCustomContextMiddleware):
    def set_context(self, request: Request) -> dict:
        return {
            "correlation_id": request.headers.get("X-Correlation-ID", uuid4().hex),
            "request_id": request.headers.get("X-Request-ID", uuid4().hex),
        }


class AdditionalUpdateForGiggles(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        update_context(updated_context="from second middleware.py")
        return await call_next(request)
