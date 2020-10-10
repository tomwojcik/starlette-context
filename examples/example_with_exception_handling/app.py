from typing import Union

import uvicorn
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.middleware import Middleware
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from examples.example_with_exception_handling.logger import log
from starlette_context import middleware, plugins


class ExceptionHandlingMiddleware(BaseHTTPMiddleware):
    @staticmethod
    async def exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        return JSONResponse(
            content={"msg": "Internal server error - on purpose!"},
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
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
            return await self.exception_handler(request, e)

        log.info("no exc raised")
        return response


# middleware order is important! exc handler has to be topmost
middleware = [
    Middleware(
        middleware.ContextMiddleware,
        plugins=(
            plugins.CorrelationIdPlugin(),
            plugins.RequestIdPlugin(),
            plugins.DateHeaderPlugin(),
            plugins.ForwardedForPlugin(),
            plugins.UserAgentPlugin(),
        ),
    ),
    Middleware(ExceptionHandlingMiddleware),
]

app = Starlette(debug=True, middleware=middleware)


@app.route("/")
async def index(request: Request):
    log.info("pre exception")
    _ = 1 / 0
    return JSONResponse({"wont reach this place": None})


uvicorn.run(app, host="0.0.0.0")
