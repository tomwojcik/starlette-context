# Context Object

The core of starlette-context is the `context` object, which provides a request-scoped data store accessible throughout your application.

## Context Implementation

The `context` object is implemented using Python's `ContextVar`, introduced in Python 3.7. It's designed to be:

- Thread-safe and async-compatible
- Available throughout the request-response cycle
- Accessible from any part of your application without passing it explicitly

The inspiration was to create something similar to Flask's `g` object or Django's middleware-based request information stores like `django-currentuser` or `django-crum`.

## Dictionary-like Interface

The `context` object behaves like a standard Python dictionary, with a few small differences:

```python
from starlette_context import context

# Set values
context["user_id"] = "12345"
context["is_admin"] = True

# Get values
user_id = context["user_id"]  # "12345"
is_admin = context.get("is_admin", False)  # True

# Check if a key exists
if "user_id" in context:
    print("User ID is set")

# Iterate over items
for key, value in context.items():
    print(f"{key}: {value}")

# Unpack into a function
def process_user(user_id, is_admin):
    # ...
    pass

process_user(**context)  # Unpacks into kwargs
```

The main difference from a standard dictionary is that you cannot serialize the context object directly. Instead, use `.data` to get a standard dictionary:

```python
import json
from starlette_context import context

# This won't work
# json_data = json.dumps(context)  # Error!

# This works
json_data = json.dumps(context.data)
```

## Accessing Context Data

To make the context available during a request-response cycle, you need to either:

1. Use one of the provided middlewares (`ContextMiddleware` or `RawContextMiddleware`)
2. Use the `request_cycle_context` context manager directly

The middleware approach is the most common and provides additional capabilities through plugins.

### Using Middleware

```python
from starlette.middleware import Middleware
from starlette.applications import Starlette
from starlette_context.middleware import ContextMiddleware

app = Starlette(middleware=[Middleware(ContextMiddleware)])
```

### Using the Context Manager

The `request_cycle_context` can be used directly in specific cases, such as in FastAPI dependency functions or unit tests:

```python
from starlette_context import request_cycle_context, context

# Use in a test
async def test_with_context():
    with request_cycle_context({"initial_data": "value"}):
        context["test_key"] = "test_value"
        assert context["initial_data"] == "value"
        assert context["test_key"] == "test_value"
    
    # Outside the context manager, context is no longer available
    # Using context here would raise ContextDoesNotExistError
```

## Context Errors

If you attempt to access the context outside of a request-response cycle or without setting up the middleware, you'll encounter a `ContextDoesNotExistError`. See the [Error Handling](./errors.md) section for more details on handling this and other exceptions.

## Helper Methods

The context object provides a few helper methods beyond standard dictionary operations:

- `context.exists()`: Check if context exists for the current async task
- `context.copy()`: Create a read-only copy of the context data