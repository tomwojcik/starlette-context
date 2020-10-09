import pytest
from starlette.applications import Starlette
from starlette.middleware import Middleware

from starlette_context.middleware import (
    ContextMiddleware,
    RawContextMiddleware,
)


class NotAPlugin:
    pass


def test_context_middleware_wrong_plugin():
    with pytest.raises(TypeError):
        Starlette(
            middleware=[Middleware(ContextMiddleware, plugins=(NotAPlugin(),))]
        )


def test_raw_middleware_wrong_plugin():
    with pytest.raises(TypeError):
        Starlette(
            middleware=[
                Middleware(RawContextMiddleware, plugins=(NotAPlugin(),))
            ]
        )
