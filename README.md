[![Test Suite](https://github.com/tomwojcik/starlette-context/actions/workflows/test-suite.yml/badge.svg)](https://github.com/tomwojcik/starlette-context/actions/workflows/test-suite.yml)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![PyPI version](https://badge.fury.io/py/starlette-context.svg)](https://badge.fury.io/py/starlette-context)
[![codecov](https://codecov.io/gh/tomwojcik/starlette-context/branch/master/graph/badge.svg)](https://codecov.io/gh/tomwojcik/starlette-context)
[![Docs](https://readthedocs.org/projects/pip/badge/?version=latest)](https://starlette-context.readthedocs.io/)
![Downloads](https://img.shields.io/pypi/dm/starlette-context)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/tomwojcik/starlette-context.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/tomwojcik/starlette-context/context:python)

# starlette context
Middleware for Starlette that allows you to store and access the context data of a request. Can be used with logging so logs automatically use request headers such as x-request-id or x-correlation-id.

Resources:

* **Source**: https://github.com/tomwojcik/starlette-context
* **Documentation**: https://starlette-context.readthedocs.io/
* **Changelog**: https://starlette-context.readthedocs.io/en/latest/changelog.html

### Installation

`$ pip install starlette-context`


### Requirements
Python 3.7+

### Dependencies

- `starlette`

All other dependencies from `requirements-dev.txt` are only needed to run tests or examples.

### Example

```python
import uvicorn

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from starlette_context import context, plugins
from starlette_context.middleware import RawContextMiddleware

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


@app.route("/")
async def index(request: Request):
    return JSONResponse(context.data)


uvicorn.run(app, host="0.0.0.0")

```
In this example the response contains a json with
```json
{
  "X-Correlation-ID":"5ca2f0b43115461bad07ccae5976a990",
  "X-Request-ID":"21f8d52208ec44948d152dc49a713fdd"
}
```

Context can be updated and accessed at anytime if it's created in the middleware.


### Contribution

See the guide on [read the docs](https://starlette-context.readthedocs.io/en/latest/contributing.html#contributing).
