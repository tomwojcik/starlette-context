import json

from starlette.applications import Starlette

from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.testclient import TestClient

from starlette_context import context, middleware


app = Starlette()
app.add_middleware(middleware.ContextMiddleware)


@app.route("/")
async def index(request: Request) -> Response:
    return JSONResponse({"exists": context.exists()})


client = TestClient(app)


def test_context_existence_in_request_response_cycle():
    resp = client.get("/")
    assert json.loads(resp.content) == {"exists": True}


def test_context_outside_of_request_response_cycle():
    assert context.exists() is False
    resp = client.get("/")
    assert context.exists() is False
