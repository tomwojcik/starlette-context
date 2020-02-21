from uuid import uuid4

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from starlette_context.middleware import ContextMiddleware


class UuidMiddleware(ContextMiddleware):
    plugins = []

    async def set_context(self, request: Request) -> dict:
        return {"from_middleware": uuid4().hex}


app = Starlette()
app.add_middleware(UuidMiddleware)


@app.route("/")
async def index(request: Request):
    from starlette_context import context

    context["from_view"] = uuid4().hex
    return JSONResponse(context.data)


client = TestClient(app)


def test_context_persistence():
    first_resp = client.get("/")
    assert first_resp.status_code == 200

    second_resp = client.get("/")
    assert second_resp.status_code == 200

    assert first_resp.json()["from_view"] != second_resp.json()["from_view"]
    assert (
        first_resp.json()["from_middleware"]
        != second_resp.json()["from_middleware"]
    )
