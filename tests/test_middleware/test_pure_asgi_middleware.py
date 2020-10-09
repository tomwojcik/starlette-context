import pytest
from starlette import status
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.testclient import TestClient
from starlette_context.header_keys import HeaderKeys

from starlette_context import plugins, context

from starlette_context.middleware import RawContextMiddleware

plugins_to_use = (
    plugins.CorrelationIdPlugin(),
    plugins.RequestIdPlugin(),
    plugins.UserAgentPlugin(),
    plugins.ForwardedForPlugin(),
    plugins.DateHeaderPlugin(),
)

middleware = [Middleware(RawContextMiddleware, plugins=plugins_to_use,)]

app = Starlette(middleware=middleware)
client = TestClient(app)


@app.route("/")
async def index(request: Request) -> JSONResponse:
    return JSONResponse(content=context.data)


def test_valid_request():
    resp = client.get("/")

    assert resp.status_code == status.HTTP_200_OK

    for plugin in plugins_to_use:
        assert plugin.key in resp.text

    assert HeaderKeys.correlation_id in resp.headers
    assert HeaderKeys.request_id in resp.headers


def test_not_a_plugin_in_init():
    class NotAPlugin:
        pass

    middleware = [Middleware(NotAPlugin,)]
    with pytest.raises(TypeError):
        Starlette(middleware=middleware)
