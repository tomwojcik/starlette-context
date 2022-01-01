from unittest import mock

from starlette import status
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.testclient import TestClient

from starlette_context import plugins
from starlette_context.errors import StarletteContextException
from starlette_context.header_keys import HeaderKeys
from starlette_context.middleware import (
    RawContextMiddleware,
    ContextMiddleware,
)
import pytest


@pytest.mark.parametrize(
    "middleware_class", [RawContextMiddleware, ContextMiddleware]
)
def test_default_error_parse(middleware_class):
    middleware = [
        Middleware(
            middleware_class,
            plugins=(plugins.CorrelationIdPlugin(),),
        )
    ]
    app = Starlette(middleware=middleware)
    client = TestClient(app)

    @app.route("/")
    async def index(request: Request) -> Response:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    response = client.get(
        "/", headers={HeaderKeys.correlation_id: "invalid_uuid"}
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert HeaderKeys.correlation_id not in response.headers
    assert (
        response.content == b"Invalid UUID in request header X-Correlation-ID"
    )


@pytest.mark.parametrize(
    "middleware_class", [RawContextMiddleware, ContextMiddleware]
)
def test_return_lib_exc_as_json(middleware_class):
    def starlette_context_error_handler(
        e: StarletteContextException,
    ) -> JSONResponse:
        return JSONResponse(
            {"error_message": e.detail}, status_code=e.status_code
        )

    middleware = [
        Middleware(
            middleware_class,
            plugins=(plugins.CorrelationIdPlugin(),),
            error_handler=starlette_context_error_handler,
        )
    ]
    app = Starlette(middleware=middleware)
    client = TestClient(app)

    @app.route("/")
    async def index(request: Request) -> Response:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    response = client.get(
        "/", headers={HeaderKeys.correlation_id: "invalid_uuid"}
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert HeaderKeys.correlation_id not in response.headers
    assert (
        response.content == b'{"error_message":'
        b'"Invalid UUID in request header X-Correlation-ID"}'
    )


@pytest.mark.parametrize(
    "middleware_class", [RawContextMiddleware, ContextMiddleware]
)
@mock.patch(
    "starlette_context.middleware.mixin."
    "StarletteContextMiddlewareMixin.get_logger"
)
def test_dont_log_errors(get_logger, middleware_class):
    middleware = [
        Middleware(
            middleware_class,
            plugins=(plugins.CorrelationIdPlugin(),),
            log_errors=False,
        )
    ]
    app = Starlette(middleware=middleware)
    client = TestClient(app)

    @app.route("/")
    async def index(request: Request) -> Response:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    client.get("/", headers={HeaderKeys.correlation_id: "invalid_uuid"})
    get_logger.assert_not_called()


@pytest.mark.parametrize(
    "middleware_class", [RawContextMiddleware, ContextMiddleware]
)
@mock.patch(
    "starlette_context.middleware.mixin."
    "StarletteContextMiddlewareMixin.get_logger"
)
def test_do_log_errors(get_logger, middleware_class):
    middleware = [
        Middleware(
            middleware_class,
            plugins=(plugins.CorrelationIdPlugin(),),
            log_errors=True,
        )
    ]
    app = Starlette(middleware=middleware)
    client = TestClient(app)

    @app.route("/")
    async def index(request: Request) -> Response:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    client.get("/", headers={HeaderKeys.correlation_id: "invalid_uuid"})
    get_logger.assert_called_once()
