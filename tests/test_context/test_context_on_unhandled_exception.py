from starlette import status
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.testclient import TestClient

from starlette_context.header_keys import HeaderKeys

from starlette_context import middleware, plugins


app = Starlette(
    middleware=[
        Middleware(
            middleware.ContextMiddleware, plugins=(plugins.RequestIdPlugin(),)
        )
    ]
)


@app.route("/exc")
async def index(request: Request):
    raise Exception


@app.route("/")
async def index(request: Request):
    return Response(status_code=status.HTTP_200_OK)


client = TestClient(app, raise_server_exceptions=False)


def test_context_persistence():
    resp = client.get("/")
    assert resp.status_code == 200
    assert HeaderKeys.request_id.lower() in resp.headers

    resp = client.get("/exc")
    assert resp.status_code == 500
    assert HeaderKeys.request_id.lower() not in resp.headers
