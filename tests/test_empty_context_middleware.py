from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from starlette_context import (
    CreateEmptyContextMiddleware,
    get_context,
    set_context,
)


async def index(request: Request):
    return JSONResponse(get_context())


async def context_from_view(request: Request):
    set_context(key=request.headers.get("User-Agent"))
    return JSONResponse(get_context())


routes = [Route("/", index), Route("/1", context_from_view)]

app = Starlette(debug=True, routes=routes)
app.add_middleware(CreateEmptyContextMiddleware)
client = TestClient(app)


def test_no_context():
    response = client.get("/")
    assert response.status_code == 200
    assert {} == response.json()


def test_context_in_view():
    response = client.get("/1")
    assert response.status_code == 200
    assert dict(key="testclient") == response.json()
