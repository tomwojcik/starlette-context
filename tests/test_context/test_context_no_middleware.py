import pytest
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from starlette_context import context
from starlette_context.errors import ContextDoesNotExistError

app = Starlette()
client = TestClient(app)


@app.route("/")
async def index(request: Request):
    return JSONResponse(context.data)


def test_no_middleware():
    with pytest.raises(ContextDoesNotExistError):
        client.get("/")
