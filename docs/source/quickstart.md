# Quickstart

## Installation

This library's only dependency is [Starlette](https://github.com/encode/starlette). It works with all Starlette-based frameworks, including:
- [FastAPI](https://github.com/tiangolo/fastapi)
- [Responder](https://github.com/taoufik07/responder)
- [Flama](https://github.com/perdy/flama)

```bash
pip install starlette-context
```

## Basic Usage

The `context` object is accessible when:
1. You're within a request-response cycle
2. You've used either `ContextMiddleware` or `RawContextMiddleware` in your ASGI app

### Minimal Working Example

```python
# app.py
from starlette.middleware import Middleware
from starlette.applications import Starlette

from starlette_context.middleware import ContextMiddleware

middleware = [Middleware(ContextMiddleware)]
app = Starlette(middleware=middleware)
```

```python
# views.py
from starlette.requests import Request
from starlette.responses import JSONResponse

from starlette_context import context

from .app import app

@app.route("/")
async def index(request: Request):
    # Access context data
    context["user_id"] = "12345"

    # Return context data in response
    return JSONResponse(context.data)
```

## Adding Plugins

Plugins automatically populate the context with useful information from request headers:

```python
from starlette.middleware import Middleware
from starlette.applications import Starlette

from starlette_context import plugins
from starlette_context.middleware import ContextMiddleware

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

With this setup, every request will have:
- A request ID (generated if not provided in headers)
- A correlation ID (generated if not provided in headers)

These values are accessible via `context.data` and are also included in the response headers.

## Using with Logging

One of the main benefits of starlette-context is enriching your logs with request data:

```python
import logging
import structlog
from starlette_context import context

# Configure structlog to include context data
structlog.configure(
    processors=[
        # Add context data to log entries
        lambda _, __, event_dict: {**event_dict, **context.data}
    ]
)

logger = structlog.get_logger()

@app.route("/")
async def index(request: Request):
    # Log with context data automatically included
    logger.info("Processing request")
    return JSONResponse({"message": "Hello World"})
```

Now your logs will include request IDs, correlation IDs, and any other data in the context.
