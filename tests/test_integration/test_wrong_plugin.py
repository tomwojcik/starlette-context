import pytest
from starlette.applications import Starlette
from starlette_context.middleware import ContextMiddleware

app = Starlette()


class NotAPlugin:
    pass


def test_set_context_in_middlewares():
    with pytest.raises(TypeError):
        app.add_middleware(ContextMiddleware.with_plugins(NotAPlugin))
