import datetime
import json

import pytest
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.testclient import TestClient

from starlette_context import context, plugins
from starlette_context.middleware import ContextMiddleware
from tests.conftest import dummy_correlation_id, dummy_request_id


    middleware = [
        Middleware(
            ContextMiddleware,
            plugins=(
                plugins.RequestIdPlugin(),
                plugins.CorrelationIdPlugin,
                plugins.DateHeaderPlugin,
            )
        )
    ]
    app = Starlette(middleware=middleware)

    @app.route("/")
    async def index(request: Request):
        return Response()

    @app.route("/dt")
    async def dt(request: Request):
        def dt_serializator(o):
            if isinstance(o, datetime.datetime):
                return o.__str__()

        return JSONResponse(
            json.loads(json.dumps(context.data, default=dt_serializator))
        )

    client = TestClient(app)


def test_response_headers(client, headers):
    response = client.get("/", headers=headers)
    assert 2 == len(response.headers)
    cid_header = response.headers["x-correlation-id"]
    rid_header = response.headers["x-request-id"]
    assert dummy_correlation_id == cid_header
    assert dummy_request_id == rid_header


def test_date_serialization_in_contextvar(client, headers):
    response = client.get("/dt", headers=headers)
    assert response.json()["Date"] == "2020-01-01 04:27:12"
