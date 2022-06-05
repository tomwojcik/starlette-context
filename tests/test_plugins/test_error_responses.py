from typing import Type

from starlette import status
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.testclient import TestClient

from starlette_context import plugins
from starlette_context.header_keys import HeaderKeys
from starlette_context.middleware import (
    ContextMiddleware,
    RawContextMiddleware,
)


def gen_middleware_config(middleware_class: Type) -> TestClient:
    middleware = [
        Middleware(
            middleware_class,
            plugins=(plugins.RequestIdPlugin(),),
        )
    ]
    app = Starlette(middleware=middleware)
    client = TestClient(app)
    return client


def test_invalid_request_id_returns_specified_response_raw_middleware():
    client = gen_middleware_config(RawContextMiddleware)

    response = client.get("/", headers={HeaderKeys.request_id: "invalid_uuid"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert HeaderKeys.request_id not in response.headers
    assert response.content == b"Invalid UUID in request header X-Request-ID"


def test_invalid_request_id_returns_specified_response_context_middleware():
    client = gen_middleware_config(ContextMiddleware)
    response = client.get("/", headers={HeaderKeys.request_id: "invalid_uuid"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert HeaderKeys.request_id not in response.headers
    assert response.content == b"Invalid UUID in request header X-Request-ID"
