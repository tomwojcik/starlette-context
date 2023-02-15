"""Tests the context manager without using the middlewares. This feature makes
it much easier for users to also test the usage of context in a unit test
environnment, allowing to create the assumed/mocked environnment directly in a
similar way to having a middleware upstream processing a request.

On FastAPI apps, this also allows usage as part of a Depends system, out
of plugins, and alleviating the Starlette architecture making
Middlewares out of the scope of the regular exception handler.
"""
import pytest
from starlette_context import request_cycle_context, context
from starlette_context.errors import ContextDoesNotExistError


def test_context_created_within_manager():
    original_data = {"test": "success"}

    # no context yet
    with pytest.raises(ContextDoesNotExistError):
        context.get("test")
    assert not context.exists()

    with request_cycle_context(original_data):
        # context available here
        assert context["test"] == "success"

    # no context anymore
    with pytest.raises(ContextDoesNotExistError):
        context.get("test")
    assert not context.exists()


def test_can_add_within():
    original_data = {"test": "success"}

    with request_cycle_context(original_data):
        # context available here
        context["extra"] = "more"

        assert context.get("extra") == "more"
        assert context.get("test") == "success"
        assert context.get("other") is None


def test_no_initial_data():
    assert not context.exists()
    with request_cycle_context():
        assert context.exists()
    assert not context.exists()
