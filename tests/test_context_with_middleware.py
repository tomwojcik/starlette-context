from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from starlette_context import EmptyContextMiddleware


async def no_context_in_resource(request: Request):
    from starlette_context import context

    return JSONResponse(context.dict())


async def add_context_in_resource(request: Request):
    from starlette_context import context

    context["set_context_in_view"] = True
    return JSONResponse(context.dict())


class MiddlewareUsingSetContextMethod(EmptyContextMiddleware):
    def set_context(self, request: Request) -> dict:
        return {"set_context_in_middleware_using_context_method": True}


class MiddlewareUsingContextObject(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ):
        from starlette_context import context

        context["set_context_in_middleware_using_context_object"] = True
        return await call_next(request)


routes = [
    Route("/context_only_from_middleware", no_context_in_resource),
    Route("/add_context_in_view", add_context_in_resource),
]

app = Starlette(debug=True, routes=routes)
app.add_middleware(MiddlewareUsingContextObject)
app.add_middleware(MiddlewareUsingSetContextMethod)

client = TestClient(app)


def test_set_context_in_middlewares():
    response = client.get("/context_only_from_middleware")
    assert response.status_code == 200
    assert {
        "set_context_in_middleware_using_context_method": True,
        "set_context_in_middleware_using_context_object": True,
    } == response.json()


def test_set_context_in_view():
    response = client.get("/add_context_in_view")
    assert response.status_code == 200
    assert {
        "set_context_in_middleware_using_context_method": True,
        "set_context_in_middleware_using_context_object": True,
        "set_context_in_view": True,
    } == response.json()
