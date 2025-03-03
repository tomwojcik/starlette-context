# Examples

Here are comprehensive examples showing how to use starlette-context in real applications.

## Basic Example

A complete working example is available in the [example directory](https://github.com/tomwojcik/starlette-context/tree/master/example) of the repository.

```python
import structlog
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route

from starlette_context import context, plugins
from starlette_context.middleware import ContextMiddleware

logger = structlog.get_logger("starlette_context_example")


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Example logging middleware that includes context in logs.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        await logger.info("request log", request=request)
        response = await call_next(request)
        await logger.info("response log", response=response)
        return response


async def index(request: Request):
    context["custom_value"] = "This will be visible in logs"
    await logger.info("log from view")
    return JSONResponse(context.data)


async def startup_event() -> None:
    # Configure structlog to include context data
    setup_logging()


app = Starlette(
    debug=True,
    routes=[
        Route("/", index),
    ],
    middleware=[
        Middleware(
            ContextMiddleware,
            plugins=(
                plugins.CorrelationIdPlugin(),
                plugins.RequestIdPlugin(),
            ),
        ),
        Middleware(LoggingMiddleware),
    ],
    on_startup=[startup_event],
)
```

## Setting Up Logging with Context

Here's how to configure structlog to automatically include context data in your logs:

```python
from collections.abc import MutableMapping
from typing import Any

import structlog
import logging.config

from starlette_context import context


def setup_logging():
    def add_app_context(
        logger: logging.Logger,
        method_name: str,
        event_dict: MutableMapping[str, Any],
    ) -> MutableMapping[str, Any]:
        if context.exists():
            event_dict.update(context.data)
        return event_dict

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            add_app_context,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.AsyncBoundLogger,
        cache_logger_on_first_use=True,
    )

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.processors.JSONRenderer(),
            },
        },
        "handlers": {
            "json": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "json",
            },
        },
        "loggers": {
            "starlette_context_example": {
                "handlers": ["json"],
                "level": "INFO",
            },
            "uvicorn": {"handlers": ["json"], "level": "INFO"},
        },
    }
    logging.config.dictConfig(logging_config)
```

With this setup, every log entry will automatically include all context data, such as request IDs and correlation IDs.

## Sample Log Output

When you run the example application and make a request, you'll see logs like:

```json
{
  "event": "request log",
  "request": "<starlette.requests.Request object>",
  "X-Correlation-ID": "5ca2f0b43115461bad07ccae5976a990",
  "X-Request-ID": "21f8d52208ec44948d152dc49a713fdd",
  "timestamp": "2023-03-01T12:00:00.123456Z"
}

{
  "event": "log from view",
  "X-Correlation-ID": "5ca2f0b43115461bad07ccae5976a990",
  "X-Request-ID": "21f8d52208ec44948d152dc49a713fdd",
  "custom_value": "This will be visible in logs",
  "timestamp": "2023-03-01T12:00:00.234567Z"
}

{
  "event": "response log",
  "response": "<starlette.responses.JSONResponse object>",
  "X-Correlation-ID": "5ca2f0b43115461bad07ccae5976a990",
  "X-Request-ID": "21f8d52208ec44948d152dc49a713fdd",
  "custom_value": "This will be visible in logs",
  "timestamp": "2023-03-01T12:00:00.345678Z"
}
```

## Custom Middleware Example

Here's an example of a custom middleware that uses the context:

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.requests import Request
from starlette_context import context

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Extract token from header
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
            # Validate token and get user info
            user_id = validate_token(token)  # Your validation logic
            if user_id:
                # Store user info in context
                context["user_id"] = user_id
                context["is_authenticated"] = True
            else:
                context["is_authenticated"] = False
        else:
            context["is_authenticated"] = False

        # Continue with request
        response = await call_next(request)
        return response

# Add to your middleware stack
middleware = [
    Middleware(ContextMiddleware),
    Middleware(AuthMiddleware),
]
```

## Running the Example

To run the example from the repository:

```bash
cd example
pip install -r requirements.txt
uvicorn app:app --reload
```

Then visit http://localhost:8000/ in your browser or use curl:

```bash
curl http://localhost:8000/
```

You should see a JSON response with the context data and logs in your console showing the same data.
