from typing import Union
from uuid import uuid4

from requests import Request, Response
from starlette.exceptions import HTTPException
from starlette.middleware.base import RequestResponseEndpoint, BaseHTTPMiddleware
from starlette.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from context.custom.middleware import (
    PreserveCustomContextMiddleware,
    update_context,
)

from examples._5_json_logger_with_context_exception.logger import log


class SetRequestAndCorrelationIdInContext(PreserveCustomContextMiddleware):
    def set_context(self, request: Request) -> dict:
        return {
            "correlation_id": self.get_correlation_id(request),
            "request_id": self.get_request_id(request),
        }


class ExceptionMiddleware(BaseHTTPMiddleware):
    @staticmethod
    async def exception_handler(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            content={"msg": "msg"}, status_code=HTTP_500_INTERNAL_SERVER_ERROR
        )

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Union[Response, JSONResponse]:

        try:
            response = await call_next(request)

        except HTTPException as e:
            log.exception("during http", exc_info=e)
            return await self.exception_handler(request, e)

        except Exception as e:
            log.exception("during unhandled", exc_info=e)
            # sentry_sdk.capture_exception()
            return await self.exception_handler(request, e)

        log.info("no exc raised")
        return response
