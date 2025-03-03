import structlog
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from starlette_context import context, plugins
from starlette_context.middleware import RawContextMiddleware

logger = structlog.get_logger("starlette_context_example")


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Example logging middleware.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        await logger.info("request log", request=request)
        response = await call_next(request)
        await logger.info("response log", response=response)
        return response


async def index(request: Request):
    context["something else"] = "This will be visible even in the response log"
    await logger.info("log from view")
    return JSONResponse(context.data)


async def startup_event() -> None:
    from setup_logging import setup_logging

    setup_logging()


app = Starlette(
    debug=True,
    routes=[
        Route("/", index),
    ],
    middleware=[
        Middleware(
            RawContextMiddleware,
            plugins=(
                plugins.CorrelationIdPlugin(),
                plugins.RequestIdPlugin(),
            ),
        ),
        Middleware(LoggingMiddleware),
    ],
    on_startup=[startup_event],
)
