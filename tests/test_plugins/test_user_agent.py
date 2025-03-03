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
from tests.conftest import dummy_user_agent


async def index(request: Request) -> Response:
    return JSONResponse(
        {"headers": str(request.headers.get(HeaderKeys.user_agent))}
    )


app = Starlette(
    routes=[
        Route("/", index),
    ],
    middleware=[
        Middleware(
            ContextMiddleware,
            plugins=(plugins.UserAgentPlugin(),),
        )
    ],
)
client = TestClient(app)

headers = {HeaderKeys.user_agent: dummy_user_agent}


def test_valid_request_returns_proper_response():
    response = client.get("/", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert dummy_user_agent in response.text
    assert HeaderKeys.user_agent not in response.text


def test_missing_forwarded_for_header():
    response = client.get("/", headers={})
    assert response.status_code == status.HTTP_200_OK
    assert dummy_user_agent not in response.text
    assert HeaderKeys.user_agent not in response.headers
