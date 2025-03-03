# Testing with Context

Testing applications that use starlette-context requires some special considerations since the context is only available during the request-response cycle. This guide explains how to effectively test your code that relies on the context object.

## Testing Endpoints with TestClient

When using Starlette's `TestClient` (or FastAPI's, which is the same), the context is properly set up as part of the request flow:

```python
from starlette.testclient import TestClient
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.responses import JSONResponse
from starlette.routing import Route

from starlette_context import context, plugins
from starlette_context.middleware import ContextMiddleware

async def test_endpoint(request):
    # Access and modify context
    context["test_value"] = "hello"
    return JSONResponse(context.data)

app = Starlette(
    routes=[Route("/test", test_endpoint)],
    middleware=[
        Middleware(
            ContextMiddleware,
            plugins=(plugins.RequestIdPlugin(),)
        )
    ]
)

def test_context_in_endpoint():
    client = TestClient(app)
    response = client.get("/test")
    
    assert response.status_code == 200
    
    # Context data is available in the response
    data = response.json()
    assert "X-Request-ID" in data
    assert data["test_value"] == "hello"
```

## Testing Functions That Use Context

For testing functions that use the context directly, you can use the `request_cycle_context` context manager:

```python
import pytest
from starlette_context import context, request_cycle_context

def function_using_context():
    # Function that uses context
    return context.get("key", "default_value")

def test_function_using_context():
    # Create a context for the test
    with request_cycle_context({"key": "test_value"}):
        result = function_using_context()
        assert result == "test_value"
        
        # We can also modify the context
        context["another_key"] = "another_value"
        assert context["another_key"] == "another_value"
```

## Mocking the Context Object

In some cases, you might want to mock the entire context object:

```python
from unittest import mock
import pytest
from starlette_context import context
from starlette_context.errors import ContextDoesNotExistError

def test_with_mocked_context():
    # Create a mock context object
    mock_context = mock.MagicMock()
    mock_context.data = {"mocked_key": "mocked_value"}
    mock_context.get.return_value = "mocked_value"
    
    # Replace the context with our mock
    with mock.patch("your_module.context", mock_context):
        # Test your function that uses context
        from your_module import your_function
        result = your_function()
        
        # Verify context was used as expected
        mock_context.get.assert_called_with("some_key")
```

## Testing Error Handling

Test how your code handles missing context:

```python
import pytest
from starlette_context import context
from starlette_context.errors import ContextDoesNotExistError

def function_with_context_check():
    if context.exists():
        return context.get("key", "default")
    return "no context"

def test_context_does_not_exist():
    # Outside request-response cycle, no context exists
    result = function_with_context_check()
    assert result == "no context"
    
    # Accessing context directly should raise an error
    with pytest.raises(ContextDoesNotExistError):
        context["key"] = "value"
```

## Testing Plugins

To test custom plugins, you can use the context middleware with your plugin and make test requests:

```python
import pytest
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from starlette_context import context
from starlette_context.middleware import ContextMiddleware
from my_module import MyCustomPlugin

async def test_endpoint(request):
    return JSONResponse(context.data)

@pytest.fixture
def test_app():
    app = Starlette(
        routes=[Route("/test", test_endpoint)],
        middleware=[
            Middleware(
                ContextMiddleware,
                plugins=(MyCustomPlugin(),)
            )
        ]
    )
    return app

def test_custom_plugin(test_app):
    client = TestClient(test_app)
    
    # Set custom header that your plugin processes
    response = client.get("/test", headers={"X-Custom-Header": "test-value"})
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify your plugin processed the header correctly
    assert "custom_key" in data
    assert data["custom_key"] == "processed-test-value"
```

## Integration Testing

For larger integration tests:

```python
import pytest
from starlette.testclient import TestClient
from your_app import create_app

@pytest.fixture
def client():
    app = create_app()
    with TestClient(app) as client:
        yield client

def test_full_request_flow(client):
    # Make a series of requests that use context
    response1 = client.get("/first-endpoint")
    request_id = response1.json()["X-Request-ID"]
    
    # Use the request ID in the next request
    response2 = client.get(
        "/second-endpoint", 
        headers={"X-Request-ID": request_id}
    )
    
    # Verify context is maintained
    assert response2.json()["X-Request-ID"] == request_id
```

## Async Testing

For async test functions, you can use pytest-asyncio:

```python
import pytest
import asyncio
from starlette_context import request_cycle_context, context

@pytest.mark.asyncio
async def test_async_function_with_context():
    async def async_function():
        return context.get("key")
    
    with request_cycle_context({"key": "async_value"}):
        result = await async_function()
        assert result == "async_value"
```

By using these testing techniques, you can effectively verify that your application is correctly using the context object throughout your request processing flow.