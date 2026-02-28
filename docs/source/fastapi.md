# FastAPI Integration

starlette-context works seamlessly with FastAPI since FastAPI is built on top of Starlette. This page shows how to integrate starlette-context with FastAPI applications.

## Basic Setup

Here's how to add starlette-context to a FastAPI application:

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette_context import context, plugins
from starlette_context.middleware import ContextMiddleware

app = FastAPI()

# Add the middleware to the FastAPI app
app.add_middleware(
    ContextMiddleware,
    plugins=(
        plugins.RequestIdPlugin(),
        plugins.CorrelationIdPlugin()
    )
)

@app.get("/")
async def read_root(request: Request):
    # Access context data in your endpoint
    context["custom_value"] = "Added in the endpoint"
    return JSONResponse(context.data)
```

## Using with Dependency Injection

FastAPI's dependency injection system works perfectly with starlette-context. You can create dependencies that use the context:

```python
from typing import Any
from fastapi import FastAPI, Depends, HTTPException, Request
from starlette_context import context, plugins
from starlette_context.middleware import ContextMiddleware

app = FastAPI()

app.add_middleware(
    ContextMiddleware,
    plugins=(
        plugins.RequestIdPlugin(),
        plugins.CorrelationIdPlugin(),
    )
)

# Define a dependency that uses context
def get_current_user():
    user_id = context.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )
    return {"user_id": user_id}

@app.get("/user/me")
async def read_user_me(current_user: dict[str, Any] = Depends(get_current_user)):
    return current_user

@app.get("/items/")
async def read_items(request: Request):
    # Store something in context
    context["user_id"] = "example_user_id"
    return JSONResponse(context.data)
```

## Using with Background Tasks

**Important**: While context may appear to be available in background tasks due to Python's `ContextVar` inheritance mechanism (PEP 567), **you should not rely on this behavior**. Always explicitly copy and pass context data to background tasks.

### Why Context Appears Available (But You Shouldn't Use It)

When a background task is created, Python's `asyncio` automatically creates a copy of the current context for the task. This means you might observe that context data is accessible within background tasks. However:

1. **This is an implementation detail**, not a guaranteed API feature
2. **Timing-sensitive**: Context availability depends on when the asyncio task is created
3. **Not officially supported**: Future versions of Python or Starlette could change this behavior
4. **Not documented as reliable**: This library does not guarantee context persistence in background tasks

### Recommended Pattern: Explicit Context Copying

Always use the explicit pattern shown below:

```python
from fastapi import FastAPI, BackgroundTasks
from starlette_context import context, request_cycle_context
from starlette_context.middleware import ContextMiddleware

app = FastAPI()
app.add_middleware(ContextMiddleware)

def process_item(item_id: str, context_data: dict):
    # ✅ RECOMMENDED: Use explicitly passed context data
    # This is reliable and guaranteed to work
    print(f"Processing item {item_id} with context: {context_data}")
    request_id = context_data.get("X-Request-ID")

@app.post("/items/{item_id}")
async def create_item(item_id: str, background_tasks: BackgroundTasks):
    # Capture context data during request
    context_data = context.data.copy()

    # Pass context data explicitly to the background task
    background_tasks.add_task(process_item, item_id, context_data)

    return {"message": "Item will be processed"}
```

### What NOT to Do

```python
# ❌ NOT RECOMMENDED: Accessing context directly in background task
def risky_background_task(item_id: str):
    # This might work now due to ContextVar inheritance,
    # but it's not guaranteed and could break in the future
    request_id = context.get("X-Request-ID")  # Risky!
    print(f"Processing {item_id} with {request_id}")

@app.post("/items/{item_id}")
async def create_item_risky(item_id: str, background_tasks: BackgroundTasks):
    # Don't rely on context being available in the background task
    background_tasks.add_task(risky_background_task, item_id)
    return {"message": "Item will be processed"}
```

## With Custom Error Handlers

When using FastAPI's exception handlers, you need to be careful with context access:

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette_context import context
from starlette_context.middleware import ContextMiddleware
from starlette_context.errors import ContextDoesNotExistError

app = FastAPI()
app.add_middleware(ContextMiddleware)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # Safely access context in exception handler
    extra_data = {}
    try:
        if context.exists():
            extra_data = {"request_id": context.get("X-Request-ID")}
    except ContextDoesNotExistError:
        pass

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail,
            **extra_data
        }
    )

@app.get("/error")
async def trigger_error():
    context["before_error"] = "This will be visible in the error response"
    raise HTTPException(status_code=400, detail="Test error")
```

## Pydantic Integration

You can use starlette-context with Pydantic for request validation:

```python
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from starlette_context import context
from starlette_context.middleware import ContextMiddleware

app = FastAPI()
app.add_middleware(ContextMiddleware)

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.post("/items/")
async def create_item(item: Item):
    # Store the validated item data in context
    context["item"] = item.dict()

    # Create response that includes context data
    return {
        "item": item,
        "request_id": context.get("X-Request-ID"),
        "stored_in_context": context.get("item")
    }
```

## Performance Considerations

When using starlette-context with FastAPI in high-performance applications:

1. Use `ContextMiddleware` for most cases, unless you have specific needs for the raw ASGI interface
2. Only include plugins you actually need to minimize overhead
3. For logging, consider batching context updates rather than updating on every log call

These strategies will help maintain FastAPI's high performance while still gaining the benefits of request context tracking.
