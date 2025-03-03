import pytest
from starlette.applications import Starlette
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from starlette_context.middleware import ContextMiddleware


class MiddlewareUsingSetContextMethod(ContextMiddleware):
    plugins = []

    async def set_context(self, request: Request) -> dict:
        return {"set_context_in_middleware_using_context_method": True}


class MiddlewareUsingContextObject(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ):
        from starlette_context import context

        context["set_context_in_middleware_using_context_object"] = True
        return await call_next(request)


async def no_context_in_resource(request: Request):
    from starlette_context import context

    return JSONResponse(context.data)


async def add_context_in_resource(request: Request):
    from starlette_context import context

    context["set_context_in_view"] = True
    return JSONResponse(context.data)


app = Starlette(
    routes=[
        Route("/context_only_from_middleware", no_context_in_resource),
        Route("/add_context_in_view", add_context_in_resource),
    ]
)
app.add_middleware(MiddlewareUsingContextObject)
app.add_middleware(MiddlewareUsingSetContextMethod)


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_set_context_in_middlewares(client):
    response = client.get("/context_only_from_middleware")
    assert response.status_code == 200
    assert {
        "set_context_in_middleware_using_context_method": True,
        "set_context_in_middleware_using_context_object": True,
    } == response.json()


def test_set_context_in_view(client):
    response = client.get("/add_context_in_view")
    assert response.status_code == 200
    assert {
        "set_context_in_middleware_using_context_method": True,
        "set_context_in_middleware_using_context_object": True,
        "set_context_in_view": True,
    } == response.json()
