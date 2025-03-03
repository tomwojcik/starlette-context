import pytest
from starlette import status
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route
from starlette.testclient import TestClient

from starlette_context import context, middleware, plugins
from starlette_context.header_keys import HeaderKeys


class CustomExc(Exception):
    pass


def custom_exc_handler(request: Request, exc):
    return Response(status_code=400, headers=context.data)


async def exc_endpoint(request: Request):
    raise Exception


async def handled_endpoint(request: Request):
    raise CustomExc


async def index_endpoint(request: Request):
    return Response(status_code=status.HTTP_200_OK)


app = Starlette(
    routes=[
        Route("/exc", exc_endpoint),
        Route("/handled", handled_endpoint),
        Route("/", index_endpoint),
    ],
    middleware=[
        Middleware(
            middleware.RawContextMiddleware,
            plugins=(plugins.RequestIdPlugin(),),
        )
    ],
    exception_handlers={CustomExc: custom_exc_handler},
)


@pytest.fixture
def client():
    with TestClient(app, raise_server_exceptions=False) as client:
        yield client


def test_context_persistence(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert HeaderKeys.request_id.lower() in resp.headers

    resp = client.get("/exc")
    assert resp.status_code == 500
    assert HeaderKeys.request_id.lower() not in resp.headers

    resp = client.get("/handled")
    assert resp.status_code == 400
    assert HeaderKeys.request_id.lower() in resp.headers
