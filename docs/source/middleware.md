# Middleware

## Purpose

The middleware creates and manages the context for each request. It's essential to configure your app to use one of the context middlewares to access the context data throughout the request lifecycle.

Detailed usage examples with plugins can be found in the [Plugins](./plugins.md) section.

## Available Middlewares

starlette-context provides two middleware implementations:

### ContextMiddleware

The `ContextMiddleware` is built on Starlette's `BaseHTTPMiddleware`. It's simple to use and provides a clean interface for context management:

```python
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette_context.middleware import ContextMiddleware
from starlette_context import plugins

middleware = [
    Middleware(
        ContextMiddleware,
        plugins=(
            plugins.RequestIdPlugin(),
            plugins.CorrelationIdPlugin()
        )
    )
]

app = Starlette(middleware=middleware)
```

### RawContextMiddleware

The `RawContextMiddleware` operates at a lower ASGI level and avoids some of the limitations of `BaseHTTPMiddleware`. It's particularly useful when working with streaming responses:

```python
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette_context.middleware import RawContextMiddleware
from starlette_context import plugins

middleware = [
    Middleware(
        RawContextMiddleware,
        plugins=(
            plugins.RequestIdPlugin(),
            plugins.CorrelationIdPlugin()
        )
    )
]

app = Starlette(middleware=middleware)
```

## Choosing the Right Middleware

Both middlewares provide the same core functionality, but have different implementations:

- **ContextMiddleware**:
  - Simpler to understand and use
  - Built on Starlette's `BaseHTTPMiddleware`
  - Works well for most use cases

- **RawContextMiddleware**:
  - Works at a lower ASGI level
  - Better performance with streaming responses
  - Doesn't have the same memory issues with large responses

For most applications, either middleware will work fine. If you're using `StreamingResponse` or dealing with large responses, consider using `RawContextMiddleware`.

## Error Handling in Middlewares

When a validation error occurs in a plugin during request processing, the middleware needs to return an error response. Starlette doesn't allow middleware to use the regular error handler (see [Starlette documentation](https://www.starlette.io/exceptions/#errors-and-handled-exceptions)), so the middleware has to send a response itself.

By default, the response will be a 400 status code with no body or extra headers (using `Response(status_code=400)`). You can customize this response at both middleware and plugin levels.

### Custom Error Responses

You can provide a custom error response when initializing the middleware:

```python
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

middleware = [
    Middleware(
        ContextMiddleware,
        default_error_response=JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error": "Invalid request"},
        ),
        plugins=(
            # your plugins...
        )
    )
]
```

Plugins can also provide their own error responses, which take precedence over the middleware's default error response.

## Exception Handling Limitation

Due to how Starlette handles application exceptions, the `enrich_response` method won't run and the default error response won't be used after an unhandled exception.

Therefore, these middlewares can't set response headers for 500 responses. You can use your own 500 handler, but be aware that the context may not be available in exception handlers.

## Middleware Mechanics

1. The middleware creates an empty "storage" bound to the context of your async request
2. The `set_context` method populates this storage with data from plugins
3. When the response is created, plugins can add headers based on context values
4. Finally, the request context is cleaned up

You can customize the context creation by either:
- Using plugins to add data to the context
- Overriding the middleware's `set_context` method to add custom data

```python
class CustomContextMiddleware(ContextMiddleware):
    async def set_context(self, request: Request) -> dict:
        # Get the standard context from plugins
        context = await super().set_context(request)

        # Add custom data
        context["environment"] = os.environ.get("ENVIRONMENT", "development")
        context["app_version"] = "1.0.0"

        return context
```
