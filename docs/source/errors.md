# Handling Errors

starlette-context provides several error types that help identify and handle issues in your application.

## ContextDoesNotExistError

This is the most common error you'll encounter, raised when you try to access the `context` object outside of a request-response cycle.

### Common Causes

#### 1. Context Not Created

The most basic cause is trying to use the `context` object without adding one of the context middlewares to your application.

```python
# This will fail with ContextDoesNotExistError
from starlette_context import context
value = context["key"]  # Error!
```

Make sure you've added either `ContextMiddleware` or `RawContextMiddleware` to your application:

```python
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette_context.middleware import ContextMiddleware

app = Starlette(middleware=[Middleware(ContextMiddleware)])
```

#### 2. Incorrect Middleware Order

The order of middlewares matters. The context is only available after the context middleware has processed the request and before it processes the response:

```python
class FirstMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Can't access context here!
        return await call_next(request)

class SecondMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Context is available here
        response = await call_next(request)
        # Context is still available here
        return response

middlewares = [
    Middleware(ContextMiddleware),  # Creates context
    Middleware(FirstMiddleware),    # Can't use context (runs before ContextMiddleware)
    Middleware(SecondMiddleware),   # Can use context (runs after ContextMiddleware)
]
```

For more details on middleware execution order, see [Starlette issue #479](https://github.com/encode/starlette/issues/479).

#### 3. Outside Request-Response Cycle

The context is only available during the request-response cycle. It doesn't persist after the response is sent:

```python
@app.route("/")
async def handler(request):
    context["value"] = "test"
    return JSONResponse({"message": "OK"})

# After the response is sent:
# context["value"]  # Would raise ContextDoesNotExistError
```

This applies to:
- Background tasks running after the response
- Logging outside of request handlers
- Testing code that checks context after a request completes

### Safe Access

Use `context.exists()` to check if the context is available before accessing it:

```python
def log_with_context(message):
    if context.exists():
        logger.info(f"{message}", extra=context.data)
    else:
        logger.info(f"{message}")
```

For testing, either:
- Return context data in the response: `return JSONResponse(context.data)`
- Use the `request_cycle_context` context manager in tests:

```python
from starlette_context import request_cycle_context, context

def test_with_context():
    with request_cycle_context({"initial": "value"}):
        context["test"] = "value"
        assert context["test"] == "value"
```

## MiddleWareValidationError

This error is raised when a plugin encounters invalid data and needs to return an error response. It's typically used within plugin implementations:

```python
from starlette.responses import JSONResponse
from starlette_context.errors import MiddleWareValidationError

async def process_request(self, request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        error_response = JSONResponse(
            {"error": "Missing authorization header"}, 
            status_code=401
        )
        raise MiddleWareValidationError(
            "Missing auth header", 
            error_response=error_response
        )
    return auth_header
```

When this error is raised in a plugin, the middleware will catch it and return the provided error response.

## ConfigurationError

This error is raised when there's an issue with the configuration of the middleware or plugins:

```python
from starlette_context.errors import ConfigurationError

# Raised when a plugin instance is invalid
if not isinstance(plugin, Plugin):
    raise ConfigurationError(f"Plugin {plugin} is not a valid instance")
```

This is typically an issue you'll encounter during development when setting up the middleware incorrectly.