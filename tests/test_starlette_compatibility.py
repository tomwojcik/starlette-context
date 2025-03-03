"""
Tests to ensure compatibility with the latest Starlette version.
"""

import importlib.metadata

import pytest
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK
from starlette.testclient import TestClient

from starlette_context import context, plugins
from starlette_context.middleware import (
    ContextMiddleware,
    RawContextMiddleware,
)


@pytest.fixture
def starlette_version():
    """
    Get the installed Starlette version.
    """
    return importlib.metadata.version("starlette")


def test_starlette_version(starlette_version):
    """
    Verify the test is running with the expected Starlette version.
    """
    # This reminds us to check compatibility when Starlette is updated
    print(f"Testing with Starlette version: {starlette_version}")
    assert starlette_version.split(".")[0] >= "0"


@pytest.fixture
def context_app():
    """
    Create a test application with ContextMiddleware.
    """

    async def homepage(request):
        context["test_key"] = "test_value"
        return JSONResponse({"context": context.data})

    # Create middleware instance directly to avoid middleware argument issues
    app = Starlette(routes=[Route("/", homepage)])

    # Add middleware directly using the app.add_middleware method
    app.add_middleware(
        ContextMiddleware,
        plugins=(
            plugins.RequestIdPlugin(),
            plugins.CorrelationIdPlugin(),
        ),
    )

    return app


@pytest.fixture
def raw_context_app():
    """
    Create a test application with RawContextMiddleware.
    """

    async def homepage(request):
        context["test_key"] = "test_value"
        return JSONResponse({"context": context.data})

    # Create middleware instance directly to avoid middleware argument issues
    app = Starlette(routes=[Route("/", homepage)])

    # Add middleware directly using the app.add_middleware method
    app.add_middleware(
        RawContextMiddleware,
        plugins=(
            plugins.RequestIdPlugin(),
            plugins.CorrelationIdPlugin(),
        ),
    )

    return app


def test_context_middleware_initialization(context_app):
    """
    Test that the ContextMiddleware initializes correctly.
    """
    with TestClient(context_app) as client:
        response = client.get("/")
        assert response.status_code == HTTP_200_OK

        data = response.json()["context"]
        assert "test_key" in data
        assert data["test_key"] == "test_value"
        assert plugins.RequestIdPlugin.key in data
        assert plugins.CorrelationIdPlugin.key in data


def test_raw_context_middleware_initialization(raw_context_app):
    """
    Test that the RawContextMiddleware initializes correctly.
    """
    with TestClient(raw_context_app) as client:
        response = client.get("/")
        assert response.status_code == HTTP_200_OK

        data = response.json()["context"]
        assert "test_key" in data
        assert data["test_key"] == "test_value"
        assert plugins.RequestIdPlugin.key in data
        assert plugins.CorrelationIdPlugin.key in data


def test_middleware_response_headers(raw_context_app):
    """
    Test that middleware adds the expected headers to the response.
    """
    with TestClient(raw_context_app) as client:
        response = client.get("/")
        assert response.status_code == HTTP_200_OK

        # Check that the expected headers are set in the response
        assert plugins.RequestIdPlugin.key.lower() in response.headers
        assert plugins.CorrelationIdPlugin.key.lower() in response.headers
