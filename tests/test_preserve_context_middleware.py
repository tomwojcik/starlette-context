from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from starlette_context import get_context, PreserveCustomContextMiddleware


async def index(request: Request):
    return JSONResponse(get_context())


routes = [Route("/", index)]

app = Starlette(debug=True, routes=routes)
app.add_middleware(PreserveCustomContextMiddleware)
client = TestClient(app)


def test_context_from_middleware():
    cid_value = "cid_value"
    rid_value = "rid_value"
    headers = {
        PreserveCustomContextMiddleware.cid: cid_value,
        PreserveCustomContextMiddleware.rid: rid_value,
        PreserveCustomContextMiddleware.date: None,
        PreserveCustomContextMiddleware.forwarded_for: None,
    }

    response = client.get("/", headers=headers)
    assert response.status_code == 200

    expected_resp = {
        **headers,
        PreserveCustomContextMiddleware.ua: "testclient",
    }
    assert expected_resp == response.json()
