[![Build Status](https://travis-ci.org/tomwojcik/starlette-context.svg?branch=master)](https://travis-ci.org/tomwojcik/starlette-context)
[![](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![PyPI version](https://badge.fury.io/py/starlette-context.svg)](https://badge.fury.io/py/starlette-context)
[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)
[![codecov](https://codecov.io/gh/tomwojcik/starlette-context/branch/master/graph/badge.svg)](https://codecov.io/gh/tomwojcik/starlette-context)

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
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse

import uvicorn
from starlette_context import context, plugins
from starlette_context.middleware import ContextMiddleware


app = Starlette(debug=True)
app.add_middleware(ContextMiddleware.with_plugins(  # easily extensible
    plugins.RequestIdPlugin,  # request id
    plugins.CorrelationIdPlugin  # correlation id
))


@app.route('/')
async def index(request: Request):
    return JSONResponse(context.data)


uvicorn.run(app, host="0.0.0.0")
```
In this example the response containes a json with
```json
{
  "X-Correlation-ID":"5ca2f0b43115461bad07ccae5976a990",
  "X-Request-ID":"21f8d52208ec44948d152dc49a713fdd"
}
```

Context can be updated and accessed at anytime if it's created in the middleware.


### Contribution
All tickets or PRs are more than welcome.
