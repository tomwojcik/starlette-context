# Plugins

Plugins allow you to extract data from requests and store it in the context object. They provide a flexible way to populate your context with standard information like request IDs or custom data specific to your application.

## Plugin Configuration

To use plugins, pass them to the middleware when initializing your application:

```python
from starlette.applications import Starlette
from starlette.middleware import Middleware
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

You can use the middleware without any plugins if you just want to create an empty context that you'll populate yourself.

## Built-in Plugins

starlette-context includes the following plugins, all accessible from the `plugins` module:

| Plugin | Class Name | Header Key | Notes |
|--------|------------|------------|-------|
| API Key | ApiKeyPlugin | X-API-Key | Extracts API key from header |
| Correlation ID | CorrelationIdPlugin | X-Correlation-ID | UUID plugin, generates value if missing |
| Date Header | DateHeaderPlugin | Date | Stores as datetime object |
| Forwarded For | ForwardedForPlugin | X-Forwarded-For | Extracts client IP |
| Request ID | RequestIdPlugin | X-Request-ID | UUID plugin, generates value if missing |
| User Agent | UserAgentPlugin | User-Agent | Extracts browser/client info |

> **Note:** Headers are case-insensitive, as per [RFC9110](https://www.rfc-editor.org/rfc/rfc9110.html#name-field-names).

You can access the header value through the plugin's `key` attribute or through the `starlette_context.header_keys.HeaderKeys` enum:

```python
from starlette_context import context
from starlette_context.plugins import RequestIdPlugin
from starlette_context.header_keys import HeaderKeys

# These are equivalent:
request_id = context[RequestIdPlugin.key]
request_id = context[HeaderKeys.request_id]
request_id = context["X-Request-ID"]
```

## UUID Plugins

The UUID plugins (`RequestIdPlugin` and `CorrelationIdPlugin`) have additional options:

- `force_new_uuid=True`: Always generate a new UUID, even if one exists in the request headers
- `validate=False`: Skip UUID validation (by default, they verify the header value is a valid UUID)
- `error_response=Response(...)`: Custom error response if UUID validation fails

Example:

```python
from starlette.responses import JSONResponse
from starlette_context.plugins import RequestIdPlugin

plugin = RequestIdPlugin(
    force_new_uuid=False,  # Use existing header if present
    validate=True,         # Validate it's a proper UUID
    error_response=JSONResponse(
        status_code=400, 
        content={"error": "Invalid request ID format"}
    )
)
```

## Creating Custom Plugins

You can create custom plugins with varying levels of complexity:

### Basic Plugin

For simple header extraction, just define a class with the header key:

```python
from starlette_context.plugins import Plugin

class AcceptLanguagePlugin(Plugin):
    key = "Accept-Language"
```

The header's value will be stored in the context under the key "Accept-Language".

### Intermediate Plugin

For more control, override the `process_request` method:

```python
import json
from typing import Any, Optional, Union
from starlette.requests import HTTPConnection, Request
from starlette_context.plugins import Plugin

class JsonBodyPlugin(Plugin):
    key = "request_body"
    
    async def process_request(
        self, request: Union[Request, HTTPConnection]
    ) -> Optional[Any]:
        if request.method in ("POST", "PUT", "PATCH"):
            try:
                body = await request.json()
                # Process only what we need
                return {
                    "id": body.get("id"),
                    "action": body.get("action")
                }
            except json.JSONDecodeError:
                return None
        return None
```

### Advanced Plugin

For complete control, implement both `process_request` and `enrich_response`:

```python
import base64
import logging
from typing import Any, Optional, Union

from starlette.responses import Response
from starlette.requests import HTTPConnection, Request
from starlette.types import Message

from starlette_context.plugins import Plugin
from starlette_context.errors import MiddleWareValidationError
from starlette_context import context


class SessionPlugin(Plugin):
    key = "session_cookie"

    async def process_request(
        self, request: Union[Request, HTTPConnection]
    ) -> Optional[Any]:
        # Access any part of the request
        raw_cookie = request.cookies.get("Session")
        if not raw_cookie:
            return None

        try:
            decoded_cookie = base64.b64decode(bytes(raw_cookie, encoding="utf-8"))
        except Exception as e:
            logging.error("Raw cookie couldn't be decoded", exc_info=e)
            # Create a response for the invalid cookie
            response = Response(
                content=f"Invalid cookie: {raw_cookie}", status_code=400
            )
            # Pass the response to abort processing
            raise MiddleWareValidationError("Cookie problem", error_response=response)
        return decoded_cookie

    async def enrich_response(self, arg: Union[Response, Message]) -> None:
        # Can access the populated context here
        previous_cookie = context.get(self.key)
        
        # For ContextMiddleware (Response object)
        if isinstance(arg, Response):
            if previous_cookie:
                arg.set_cookie("PreviousSession", previous_cookie)
            arg.set_cookie("Session", "SGVsbG8gV29ybGQ=")
        # For RawContextMiddleware (Message object)
        elif arg["type"] == "http.response.start":
            # Handle response headers for raw ASGI
            pass
```

> **Note:** The type of arguments received by plugin methods depends on which middleware you use:
> - With `ContextMiddleware`: `Request` and `Response` objects
> - With `RawContextMiddleware`: `HTTPConnection` and `Message` objects