# starlette context
Middleware for Starlette that allows you to store and access the context data of a request. Can be used with logging so logs automatically use request headers such as x-request-id or x-correlation-id.

### Motivation

I use FastAPI. I needed something that will allow me to log with context data. Right now I can just `log.info('Message')` and I have log (in ELK) with request id and correlation id. I don't even think about passing this data to logger. It's there automatically.
  
### Installation 

`$ pip install starlette-context`


### Requirements
Python 3.7+

For Python 3.6 only:  
`contextvar` came out with python3.7 and is required for this to run. If you need to use Starlette with python3.6, there is a backport of `contextvar` for py36. 
https://github.com/MagicStack/contextvars

### Dependencies

- `starlette`

All other dependencies from `requirements-dev.txt` are only needed to run tests or examples. Test/dev env is dockerized if you want to try them yourself.
    
### Example
**examples/simple_examples/set_context_in_middleware.py**

```python
import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route
from starlette.responses import JSONResponse
from starlette_context import BasicContextMiddleware, context  # import


async def index(request: Request):
    return JSONResponse(context.dict())  # we can access context object


routes = [
    Route('/', index)
]

app = Starlette(debug=True, routes=routes)
app.add_middleware(BasicContextMiddleware)  # we create context
uvicorn.run(app)
```
In this example the response containes a json with
```json
{
  "X-Correlation-ID":"5ca2f0b43115461bad07ccae5976a990",
  "X-Request-ID":"21f8d52208ec44948d152dc49a713fdd",
  "Date":null,
  "X-Forwarded-For":null,
  "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/73.0.3683.86 Chrome/73.0.3683.86 Safari/537.36"
}
```

Context can be updated and accessed at anytime if it's created in the middleware.


### Contribution
All tickets or PRs are more than welcome.
