from starlette import status
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.testclient import TestClient

from starlette_context import middleware, plugins, context
from starlette_context.header_keys import HeaderKeys


class CustomExc(Exception):
    pass


def custom_exc_handler(request: Request, exc):
    return Response(status_code=400, headers=context.data)


app = Starlette(
    middleware=[
        Middleware(
            middleware.RawContextMiddleware,
            plugins=(plugins.RequestIdPlugin(),),
        )
    ],
    exception_handlers={CustomExc: custom_exc_handler},
)


@app.route("/exc")
async def exc(request: Request):
    raise Exception


@app.route("/handled")
async def handled(request: Request):
    raise CustomExc


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

    resp = client.get("/handled")
    assert resp.status_code == 400
    assert HeaderKeys.request_id.lower() in resp.headers
