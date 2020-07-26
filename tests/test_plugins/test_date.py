import datetime
import pytest

from starlette import status
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.testclient import TestClient
from starlette_context.plugins import DateHeaderPlugin

from starlette_context.header_keys import HeaderKeys
from starlette_context.middleware import ContextMiddleware
from starlette_context import plugins


middleware = [
    Middleware(ContextMiddleware, plugins=(plugins.DateHeaderPlugin(),),)
]
app = Starlette(middleware=middleware)
client = TestClient(app)


@app.route("/")
async def index(request: Request) -> Response:
    return JSONResponse({"headers": str(request.headers.get(HeaderKeys.date))})


@pytest.mark.parametrize(
    "date_header",
    [
        "Wed, 01 Jan 2020 04:27:12 GMT",
        "Wed, 01 Jan 2020 04:27:12 ",
        "Wed, 01 Jan 2020 04:27:12",
    ],
)
def test_valid_request_returns_proper_response(date_header):
    response = client.get("/", headers={HeaderKeys.date: date_header})
    assert response.status_code == status.HTTP_200_OK
    assert date_header in response.text


def test_rfc1123_parsing_method():
    date_header = "Wed, 01 Jan 2020 04:27:12"
    expected_datetime = datetime.datetime(
        year=2020, month=1, day=1, hour=4, minute=27, second=12
    )
    dt = DateHeaderPlugin.rfc1123_to_dt(date_header)
    assert dt == expected_datetime


def test_invalid_date_header_raises_exception():
    with pytest.raises(ValueError):
        client.get("/", headers={HeaderKeys.date: "invalid_date"})

    with pytest.raises(ValueError):
        client.get(
            "/", headers={HeaderKeys.date: "Wed, 01 Jan 2020 04:27:12 invalid"}
        )

    allow_500_client = TestClient(app, raise_server_exceptions=False)
    response = allow_500_client.get(
        "/", headers={HeaderKeys.date: "invalid_date"}
    )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert HeaderKeys.date not in response.headers


def test_missing_header_date():
    response = client.get("/", headers={})
    assert response.status_code == status.HTTP_200_OK
    assert HeaderKeys.date not in response.headers
