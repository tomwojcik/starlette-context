import pytest
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.testclient import TestClient


async def index(request: Request):
    from starlette_context import context
    return JSONResponse(context.dict())


routes = [
    Route("/", index),
]

app = Starlette(debug=True, routes=routes)
client = TestClient(app)


def test_no_middleware():
    with pytest.raises(LookupError):
        client.get("/")
