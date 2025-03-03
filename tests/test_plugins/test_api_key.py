from starlette import status
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route
from starlette.testclient import TestClient

from starlette_context import plugins
from starlette_context.header_keys import HeaderKeys
from starlette_context.middleware import ContextMiddleware
from tests.conftest import dummy_api_key


async def index(request: Request) -> Response:
    return JSONResponse(
        {"headers": str(request.headers.get(HeaderKeys.api_key))}
    )


app = Starlette(
    routes=[
        Route("/", index),
    ],
    middleware=[
        Middleware(
            ContextMiddleware,
            plugins=(plugins.ApiKeyPlugin(),),
        )
    ],
)
client = TestClient(app)
headers = {HeaderKeys.api_key: dummy_api_key}


def test_valid_request_returns_proper_response():
    response = client.get("/", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert dummy_api_key in response.text
    assert HeaderKeys.api_key not in response.text


def test_missing_forwarded_for_header():
    response = client.get("/", headers={})
    assert response.status_code == status.HTTP_200_OK
    assert dummy_api_key not in response.text
    assert HeaderKeys.api_key not in response.headers
