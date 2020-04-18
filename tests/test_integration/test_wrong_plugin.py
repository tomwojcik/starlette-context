import pytest
from starlette.applications import Starlette
from starlette.middleware import Middleware

from starlette_context.middleware import ContextMiddleware


class NotAPlugin:
    pass


def test_set_context_in_middlewares():
    with pytest.raises(TypeError):
        Starlette(
            middleware=[Middleware(ContextMiddleware, plugins=(NotAPlugin,))]
        )
