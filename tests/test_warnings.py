"""
Temp set of tests until 1.0.0 is released.
"""

import warnings
from unittest.mock import MagicMock

from starlette_context.middleware.context_middleware import (
    CONTEXT_MIDDLEWARE_WARNING_MSG,
    ContextMiddleware,
)
from starlette_context.middleware.raw_middleware import RawContextMiddleware


def test_context_middleware_raises_warning():
    with warnings.catch_warnings(record=True) as caught_warnings:
        ContextMiddleware(app=MagicMock())
    assert len(caught_warnings) == 1
    w = caught_warnings[0]
    assert str(w.message) == CONTEXT_MIDDLEWARE_WARNING_MSG
    assert w.category == DeprecationWarning


def test_raw_context_middleware_does_not_raise_warning():
    with warnings.catch_warnings(record=True) as caught_warnings:
        RawContextMiddleware(app=MagicMock())
    assert len(caught_warnings) == 0
