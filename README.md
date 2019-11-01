# starlette-context
Middleware for Starlette (and FastAPI) that allows you to store and access request data, like correlation id or metadata.


There are a few github tickets related to this:
https://github.com/tiangolo/fastapi/issues/397
https://github.com/encode/starlette/issues/420


Example from `examples` dir:

```python
# middleware.py
from requests import Request

from context.custom.middleware import PreserveCustomContextMiddleware


class PreserveIdentifiersMiddleware(PreserveCustomContextMiddleware):
    def set_context(self, request: Request) -> dict:
        return {
            "correlation_id": self.get_correlation_id(request),
            "request_id": self.get_request_id(request),
        }
```

```python
# app.py
app = FastAPI(title="PreserveIdentifiersExample")

from .api import router

app.add_middleware(PreserveIdentifiersMiddleware)
```

```python
# api.py
from fastapi import APIRouter

from context.custom import update_context
from .logger import log

router = APIRouter()

@router.get("/")
async def index():
    log.info("test")
    update_context(yet_another_update="from api now")
    log.info("test2")
    return {"msg": "ok"}
```

In this example `log.info` will dump json log (hi ELK) to stdout with correlation id, request id and whatever is needed.
In runtime we `update_context`, so the second log will also contain `'yet_another_update': 'from api now'` in its body.

If you want to run one of the examples yourself, just make venv, install requirements and run `asgi.py`.


All tickets or PRs are more than welcome.
