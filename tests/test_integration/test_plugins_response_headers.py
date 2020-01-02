import datetime
import json

import pytest
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.testclient import TestClient

from starlette_context import context, plugins
from starlette_context.middleware import ContextMiddleware
from tests.conftest import dummy_correlation_id, dummy_request_id


@pytest.fixture(scope="function", autouse=True)
def client():
    """
    That way so `with_plugins` is cls var is clear after those tests.
    """
    app = Starlette()
    app.add_middleware(
        ContextMiddleware.with_plugins(
            plugins.RequestIdPlugin(),
            plugins.CorrelationIdPlugin,
            plugins.DateHeaderPlugin,
        )
    )

    @app.route("/index")
    async def index(request: Request):
        return Response()

    @app.route("/dt")
    async def dt(request: Request):
        def dt_serializator(o):
            if isinstance(o, datetime.datetime):
                return o.__str__()

        return JSONResponse(
            json.loads(json.dumps(context.dict(), default=dt_serializator))
        )

    return TestClient(app)


def test_response_headers(client, headers):
    response = client.get("/index", headers=headers)
    assert 2 == len(response.headers)
    cid_header = response.headers["x-correlation-id"]
    rid_header = response.headers["x-request-id"]
    assert dummy_correlation_id == cid_header
    assert dummy_request_id == rid_header


def test_date_serialization_in_contextvar(client, headers):
    response = client.get("/dt", headers=headers)
    assert response.json()["Date"] == "2020-01-01 04:27:12"
