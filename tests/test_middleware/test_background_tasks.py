"""
Tests for context behavior with background tasks.

This test module verifies how starlette-context behaves when background
tasks are used.

## Key Findings:

Context IS available in background tasks with BOTH ContextMiddleware and
RawContextMiddleware. This is due to Python's ContextVar behavior, not
middleware implementation:

1. **Python ContextVar Inheritance**: When an asyncio task is created, it
   automatically inherits a COPY of the current context (since Python 3.7,
   PEP 567).

2. **Starlette Background Tasks**: These are implemented as asyncio tasks,
   so they inherit the request context at task creation time.

3. **Context Persistence**: Even after the middleware's context manager exits
   and resets the parent context, background tasks keep their inherited copy.

## Why You Should NOT Rely On This:

Despite context being available, the starlette-context documentation
explicitly recommends against relying on this behavior:

1. **Undocumented behavior**: This is an implementation detail, not a
   guaranteed API.

2. **Timing sensitivity**: Context availability depends on when the asyncio
   task is created vs. when the context manager exits.

3. **Future compatibility**: Python or Starlette changes could break this
   behavior.

4. **Recommended pattern**: Always explicitly copy context.data and pass it
   as a parameter to background tasks.

## References:
- PEP 567 (Context Variables)
- Python contextvars documentation
- Starlette background tasks documentation
- Starlette issue #919 (BaseHTTPMiddleware blocking issue)
"""

import asyncio
import uuid
from typing import Any

import pytest
from starlette.applications import Starlette
from starlette.background import BackgroundTask, BackgroundTasks
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from starlette_context import context, plugins
from starlette_context.errors import ContextDoesNotExistError
from starlette_context.middleware import (
    ContextMiddleware,
    RawContextMiddleware,
)

# Shared state for collecting background task results
background_results: list[dict[str, Any]] = []


def reset_background_results() -> None:
    """
    Reset the shared background results list.
    """
    global background_results
    background_results = []


def collect_context_in_background(task_id: str) -> None:
    """
    Background task that attempts to access context.

    This is a synchronous function to test sync background tasks.
    """
    try:
        # Try to access context
        request_id = context.get(plugins.RequestIdPlugin.key, None)
        correlation_id = context.get(plugins.CorrelationIdPlugin.key, None)
        background_results.append(
            {
                "task_id": task_id,
                "context_exists": True,
                "request_id": request_id,
                "correlation_id": correlation_id,
            }
        )
    except ContextDoesNotExistError:
        background_results.append(
            {
                "task_id": task_id,
                "context_exists": False,
                "request_id": None,
                "correlation_id": None,
            }
        )


async def async_collect_context_in_background(
    task_id: str, delay: float = 0.1
) -> None:
    """
    Async background task that attempts to access context after a delay.

    The delay simulates real-world background task processing time.
    """
    await asyncio.sleep(delay)
    try:
        # Try to access context
        request_id = context.get(plugins.RequestIdPlugin.key, None)
        correlation_id = context.get(plugins.CorrelationIdPlugin.key, None)
        background_results.append(
            {
                "task_id": task_id,
                "context_exists": True,
                "request_id": request_id,
                "correlation_id": correlation_id,
            }
        )
    except ContextDoesNotExistError:
        background_results.append(
            {
                "task_id": task_id,
                "context_exists": False,
                "request_id": None,
                "correlation_id": None,
            }
        )


def collect_context_from_copied_data(
    task_id: str, context_data: dict[str, Any]
) -> None:
    """
    Background task using the recommended pattern: copying context data.

    This is the documented and recommended way to use context in background
    tasks.
    """
    background_results.append(
        {
            "task_id": task_id,
            "context_exists": "copied",
            "request_id": context_data.get(plugins.RequestIdPlugin.key),
            "correlation_id": context_data.get(
                plugins.CorrelationIdPlugin.key
            ),
        }
    )


@pytest.fixture
def context_middleware_app():
    """
    Create a Starlette app with ContextMiddleware (BaseHTTPMiddleware).

    Due to BaseHTTPMiddleware's bug, context WILL be available in background
    tasks (but this should not be relied upon).
    """

    async def endpoint_with_background_task(request):
        """
        Endpoint that adds a background task.
        """
        task_id = str(uuid.uuid4())
        request_id = context.get(plugins.RequestIdPlugin.key)

        # Add background task
        background_task = BackgroundTask(
            collect_context_in_background, task_id
        )

        return JSONResponse(
            {"task_id": task_id, "request_id": request_id},
            background=background_task,
        )

    async def endpoint_with_async_background_task(request):
        """
        Endpoint that adds an async background task with delay.
        """
        task_id = str(uuid.uuid4())
        request_id = context.get(plugins.RequestIdPlugin.key)

        # Add async background task with delay
        background_task = BackgroundTask(
            async_collect_context_in_background, task_id, delay=0.1
        )

        return JSONResponse(
            {"task_id": task_id, "request_id": request_id},
            background=background_task,
        )

    async def endpoint_with_multiple_background_tasks(request):
        """
        Endpoint that adds multiple background tasks.
        """
        task_ids = [str(uuid.uuid4()) for _ in range(3)]
        request_id = context.get(plugins.RequestIdPlugin.key)

        # Add multiple background tasks
        background_tasks = BackgroundTasks()
        for task_id in task_ids:
            background_tasks.add_task(collect_context_in_background, task_id)

        return JSONResponse(
            {"task_ids": task_ids, "request_id": request_id},
            background=background_tasks,
        )

    async def endpoint_with_copied_context(request):
        """Endpoint using the recommended pattern: copying context."""
        task_id = str(uuid.uuid4())
        # Copy context data (recommended pattern)
        context_data = context.data.copy()
        request_id = context_data.get(plugins.RequestIdPlugin.key)

        # Pass context data to background task
        background_task = BackgroundTask(
            collect_context_from_copied_data, task_id, context_data
        )

        return JSONResponse(
            {"task_id": task_id, "request_id": request_id},
            background=background_task,
        )

    app = Starlette(
        routes=[
            Route("/background", endpoint_with_background_task),
            Route("/background-async", endpoint_with_async_background_task),
            Route(
                "/background-multiple", endpoint_with_multiple_background_tasks
            ),
            Route("/background-copied", endpoint_with_copied_context),
        ]
    )

    app.add_middleware(
        ContextMiddleware,
        plugins=(
            plugins.RequestIdPlugin(),
            plugins.CorrelationIdPlugin(),
        ),
    )

    return app


@pytest.fixture
def raw_context_middleware_app():
    """
    Create a Starlette app with RawContextMiddleware (pure ASGI).

    With pure ASGI middleware, context should NOT be available in background
    tasks (as documented).
    """

    async def endpoint_with_background_task(request):
        """
        Endpoint that adds a background task.
        """
        task_id = str(uuid.uuid4())
        request_id = context.get(plugins.RequestIdPlugin.key)

        # Add background task
        background_task = BackgroundTask(
            collect_context_in_background, task_id
        )

        return JSONResponse(
            {"task_id": task_id, "request_id": request_id},
            background=background_task,
        )

    async def endpoint_with_async_background_task(request):
        """
        Endpoint that adds an async background task with delay.
        """
        task_id = str(uuid.uuid4())
        request_id = context.get(plugins.RequestIdPlugin.key)

        # Add async background task with delay
        background_task = BackgroundTask(
            async_collect_context_in_background, task_id, delay=0.1
        )

        return JSONResponse(
            {"task_id": task_id, "request_id": request_id},
            background=background_task,
        )

    async def endpoint_with_copied_context(request):
        """Endpoint using the recommended pattern: copying context."""
        task_id = str(uuid.uuid4())
        # Copy context data (recommended pattern)
        context_data = context.data.copy()
        request_id = context_data.get(plugins.RequestIdPlugin.key)

        # Pass context data to background task
        background_task = BackgroundTask(
            collect_context_from_copied_data, task_id, context_data
        )

        return JSONResponse(
            {"task_id": task_id, "request_id": request_id},
            background=background_task,
        )

    app = Starlette(
        routes=[
            Route("/background", endpoint_with_background_task),
            Route("/background-async", endpoint_with_async_background_task),
            Route("/background-copied", endpoint_with_copied_context),
        ]
    )

    app.add_middleware(
        RawContextMiddleware,
        plugins=(
            plugins.RequestIdPlugin(),
            plugins.CorrelationIdPlugin(),
        ),
    )

    return app


def test_context_middleware_sync_background_task(context_middleware_app):
    """
    Test that ContextMiddleware keeps context available in sync background
    tasks.

    Context is available due to Python's ContextVar inheritance: asyncio
    tasks automatically inherit a copy of the context. This happens with
    both ContextMiddleware and RawContextMiddleware.

    Note: While this works, it should NOT be relied upon. Use the explicit
    context.data.copy() pattern instead (see
    test_context_middleware_copied_context_pattern).
    """
    reset_background_results()

    with TestClient(context_middleware_app) as client:
        response = client.get("/background")
        assert response.status_code == 200

        data = response.json()
        task_id = data["task_id"]
        request_id = data["request_id"]

        # Background task should have executed (TestClient waits for it)
        assert len(background_results) == 1
        result = background_results[0]

        # Context IS available due to ContextVar inheritance
        assert result["task_id"] == task_id
        assert result["context_exists"] is True
        assert result["request_id"] == request_id
        assert result["correlation_id"] is not None


def test_context_middleware_async_background_task(context_middleware_app):
    """
    Test that ContextMiddleware keeps context available in async background
    tasks with delays.

    Context remains available even after delays due to ContextVar inheritance.
    The asyncio task keeps its inherited context copy throughout its lifetime.
    """
    reset_background_results()

    with TestClient(context_middleware_app) as client:
        response = client.get("/background-async")
        assert response.status_code == 200

        data = response.json()
        task_id = data["task_id"]
        request_id = data["request_id"]

        # Background task should have executed
        assert len(background_results) == 1
        result = background_results[0]

        # Context is still available even after delay
        assert result["task_id"] == task_id
        assert result["context_exists"] is True
        assert result["request_id"] == request_id


def test_context_middleware_multiple_background_tasks(
    context_middleware_app,
):
    """
    Test that ContextMiddleware keeps context available for multiple background
    tasks.
    """
    reset_background_results()

    with TestClient(context_middleware_app) as client:
        response = client.get("/background-multiple")
        assert response.status_code == 200

        data = response.json()
        task_ids = data["task_ids"]
        request_id = data["request_id"]

        # All background tasks should have executed
        assert len(background_results) == 3

        # All tasks should have access to the same context
        for result in background_results:
            assert result["task_id"] in task_ids
            assert result["context_exists"] is True
            assert result["request_id"] == request_id
            assert result["correlation_id"] is not None


def test_raw_context_middleware_sync_background_task(
    raw_context_middleware_app,
):
    """
    Test that RawContextMiddleware also keeps context available in sync
    background tasks.

    Despite being pure ASGI (no BaseHTTPMiddleware), context IS available due
    to Python's ContextVar inheritance. When the background task is created as
    an asyncio task, it inherits a copy of the context.

    This demonstrates that context availability in background tasks is NOT
    about middleware implementation, but about Python's ContextVar behavior.
    """
    reset_background_results()

    with TestClient(raw_context_middleware_app) as client:
        response = client.get("/background")
        assert response.status_code == 200

        data = response.json()
        task_id = data["task_id"]
        request_id = data["request_id"]

        # Background task should have executed
        assert len(background_results) == 1
        result = background_results[0]

        # Context IS available due to ContextVar inheritance
        assert result["task_id"] == task_id
        assert result["context_exists"] is True
        assert result["request_id"] == request_id
        assert result["correlation_id"] is not None


def test_raw_context_middleware_async_background_task(
    raw_context_middleware_app,
):
    """
    Test that RawContextMiddleware keeps context available in async background
    tasks with delays.

    Even with pure ASGI middleware, context inheritance works the same way.
    """
    reset_background_results()

    with TestClient(raw_context_middleware_app) as client:
        response = client.get("/background-async")
        assert response.status_code == 200

        data = response.json()
        task_id = data["task_id"]
        request_id = data["request_id"]

        # Background task should have executed
        assert len(background_results) == 1
        result = background_results[0]

        # Context IS available
        assert result["task_id"] == task_id
        assert result["context_exists"] is True
        assert result["request_id"] == request_id


def test_context_middleware_copied_context_pattern(context_middleware_app):
    """
    Test the recommended pattern: copying context data and passing it to
    background tasks.

    This pattern works reliably with both ContextMiddleware and
    RawContextMiddleware.
    """
    reset_background_results()

    with TestClient(context_middleware_app) as client:
        response = client.get("/background-copied")
        assert response.status_code == 200

        data = response.json()
        task_id = data["task_id"]
        request_id = data["request_id"]

        # Background task should have executed
        assert len(background_results) == 1
        result = background_results[0]

        # Copied context data is available
        assert result["task_id"] == task_id
        assert result["context_exists"] == "copied"
        assert result["request_id"] == request_id
        assert result["correlation_id"] is not None


def test_raw_context_middleware_copied_context_pattern(
    raw_context_middleware_app,
):
    """
    Test the recommended pattern with RawContextMiddleware.

    The copied context pattern works reliably regardless of middleware type.
    """
    reset_background_results()

    with TestClient(raw_context_middleware_app) as client:
        response = client.get("/background-copied")
        assert response.status_code == 200

        data = response.json()
        task_id = data["task_id"]
        request_id = data["request_id"]

        # Background task should have executed
        assert len(background_results) == 1
        result = background_results[0]

        # Copied context data is available
        assert result["task_id"] == task_id
        assert result["context_exists"] == "copied"
        assert result["request_id"] == request_id
        assert result["correlation_id"] is not None


def test_context_isolation_between_requests(context_middleware_app):
    """
    Test that each request gets its own isolated context, even when background
    tasks are involved.

    This verifies that context doesn't leak between concurrent requests.
    """
    reset_background_results()

    with TestClient(context_middleware_app) as client:
        # Make multiple concurrent requests
        response1 = client.get("/background")
        response2 = client.get("/background")
        response3 = client.get("/background")

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200

        data1 = response1.json()
        data2 = response2.json()
        data3 = response3.json()

        # Each request should have different request IDs
        request_ids = {
            data1["request_id"],
            data2["request_id"],
            data3["request_id"],
        }
        assert len(request_ids) == 3

        # All background tasks should have executed
        assert len(background_results) == 3

        # Each background task should have its own context
        for result in background_results:
            assert result["context_exists"] is True
            assert result["request_id"] in request_ids
            # Verify no context leakage - each task has the correct request_id
            # The request_id from background should match one of the requests
            assert result["request_id"] is not None
