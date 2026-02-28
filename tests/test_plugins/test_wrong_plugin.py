import pytest
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.testclient import TestClient

from starlette_context.errors import ConfigurationError
from starlette_context.middleware import (
    ContextMiddleware,
    RawContextMiddleware,
)
from starlette_context.plugins.base import Plugin


class NotAPlugin:
    pass


class PluginWithoutKey(Plugin):
    key = None


def test_context_middleware_wropluginsng_plugin(test_client_factory):
    with pytest.raises(ConfigurationError):
        app = Starlette()
        app.add_middleware(ContextMiddleware, plugins=[NotAPlugin()])
        with test_client_factory(app):
            pass


def test_raw_middleware_wrong_plugin(test_client_factory):
    with pytest.raises(ConfigurationError):
        app = Starlette()
        app.add_middleware(RawContextMiddleware, plugins=[NotAPlugin()])
        with test_client_factory(app):
            pass


def test_plugin_missing_key():
    middleware = [Middleware(ContextMiddleware, plugins=[PluginWithoutKey()])]
    app = Starlette(middleware=middleware)
    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/")
    assert response.status_code == 500
