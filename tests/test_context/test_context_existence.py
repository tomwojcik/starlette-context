import json

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route
from starlette.testclient import TestClient

from starlette_context import context, middleware


async def index(request: Request) -> Response:
    return JSONResponse({"exists": context.exists()})


app = Starlette(
    routes=[
        Route("/", index),
    ]
)
app.add_middleware(middleware.ContextMiddleware)


client = TestClient(app)


def test_context_existence_in_request_response_cycle():
    resp = client.get("/")
    assert json.loads(resp.content) == {"exists": True}


def test_context_outside_of_request_response_cycle():
    assert context.exists() is False
    _ = client.get("/")
    assert context.exists() is False
