from starlette import status
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.testclient import TestClient

from starlette_context import plugins
from starlette_context.header_keys import HeaderKeys
from starlette_context.middleware import ContextMiddleware
from tests.conftest import dummy_forwarded_for

middleware = [
    Middleware(
        ContextMiddleware,
        plugins=(plugins.ForwardedForPlugin(),),
    )
]
app = Starlette(middleware=middleware)
client = TestClient(app)
headers = {HeaderKeys.forwarded_for: dummy_forwarded_for}


@app.route("/")
async def index(request: Request) -> Response:
    return JSONResponse(
        {"headers": str(request.headers.get(HeaderKeys.forwarded_for))}
    )


def test_valid_request_returns_proper_response():
    response = client.get("/", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert dummy_forwarded_for in response.text
    assert HeaderKeys.forwarded_for not in response.text


def test_missing_forwarded_for_header():
    response = client.get("/", headers={})
    assert response.status_code == status.HTTP_200_OK
    assert dummy_forwarded_for not in response.text
    assert HeaderKeys.forwarded_for not in response.headers
