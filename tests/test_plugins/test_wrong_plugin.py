import pytest
from starlette.applications import Starlette

from starlette_context.errors import ConfigurationError
from starlette_context.middleware import (
    ContextMiddleware,
    RawContextMiddleware,
)


class NotAPlugin:
    pass


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
