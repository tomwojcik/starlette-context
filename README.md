# starlette-context

[![Test Suite](https://github.com/tomwojcik/starlette-context/actions/workflows/test-suite.yml/badge.svg)](https://github.com/tomwojcik/starlette-context/actions/workflows/test-suite.yml)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![PyPI version](https://badge.fury.io/py/starlette-context.svg)](https://badge.fury.io/py/starlette-context)
[![codecov](https://codecov.io/gh/tomwojcik/starlette-context/branch/master/graph/badge.svg)](https://codecov.io/gh/tomwojcik/starlette-context)
[![Docs](https://readthedocs.org/projects/pip/badge/?version=latest)](https://starlette-context.readthedocs.io/)
[![Downloads](https://img.shields.io/pypi/dm/starlette-context)](https://pypi.org/project/starlette-context/)

Middleware for Starlette that allows you to store and access the context data of a request. Can be used with logging so logs automatically use request headers such as x-request-id or x-correlation-id.

## Resources

- **Source**: https://github.com/tomwojcik/starlette-context
- **Documentation**: https://starlette-context.readthedocs.io/
- **Changelog**: https://starlette-context.readthedocs.io/en/latest/changelog.html

## Installation

```bash
# Python 3.9+
pip install starlette-context
```

## Dependencies

- `starlette>=0.27.0`

## Example

```python
import uvicorn

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from starlette_context import context, plugins
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


@app.route("/")
async def index(request: Request):
    return JSONResponse(context.data)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")
```

In this example the response contains a JSON with:

```json
{
  "X-Correlation-ID": "5ca2f0b43115461bad07ccae5976a990",
  "X-Request-ID": "21f8d52208ec44948d152dc49a713fdd"
}
```

Context can be updated and accessed at anytime if it's created in the middleware.

## Sponsorship

A huge thank you to [Adverity](https://www.adverity.com/) for sponsoring the development of this OSS library.

## Contribution

See the [contributing guide](https://starlette-context.readthedocs.io/en/latest/contributing.html).
