# starlette context
Middleware for Starlette (and FastAPI) that allows you to store and access request data, like correlation id or metadata.

### Installation 

`pip install starlette-context`


### Requirements:
only `starlette`

### Why I have created it

I use FastAPI. I needed something that will allow me to log with context data. Right now I can just `log.info('Message')` and I have log (in ELK) with request id and correlation id. I don't even think about passing this data to logger. It's there automatically.
  
    


Minimal example from `examples/simple_examples/set_context_in_middleware.py` dir:

```python
import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route
from starlette.responses import JSONResponse
from starlette_context import PreserveCustomContextMiddleware, get_context


async def index(request: Request):
    return JSONResponse(get_context())  # <-- we get context (dict)


routes = [
    Route('/', index)
]

app = Starlette(debug=True, routes=routes)
app.add_middleware(PreserveCustomContextMiddleware)  # we set context with some data
uvicorn.run(app)
```

Returns JSONResponse with data from context, such as RequestID.
Context can be updated and accessed at anytime if it's created in the middleware.

All tickets or PRs are more than welcome.
