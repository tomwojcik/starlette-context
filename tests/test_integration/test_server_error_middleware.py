import json
import uuid
from typing import NoReturn

from starlette.middleware import Middleware

from starlette_context import plugins
from starlette.applications import Starlette

from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from starlette_context import middleware
from starlette_context.header_keys import HeaderKeys
from starlette_context import context


class CustomException(Exception):
    pass


async def custom_exception_handler(request: Request, exc: Exception):
    return JSONResponse({"exception": "handled"}, headers=context.data)


async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse({"exception": "handled"}, headers=context.data)


middleware = [
    Middleware(
        middleware.ContextMiddleware, plugins=(plugins.RequestIdPlugin(),)
    )
]
exception_handlers = {
    CustomException: custom_exception_handler,
    Exception: general_exception_handler,
}


app = Starlette(exception_handlers=exception_handlers, middleware=middleware,)

headers = {HeaderKeys.request_id: uuid.uuid4().hex}


@app.route("/")
async def index(_) -> NoReturn:
    raise RuntimeError


@app.route("/custom-exc")
async def index(_) -> NoReturn:
    raise CustomException


client = TestClient(app)


def test_exception_handling_that_is_not_resulting_in_500():
    resp = client.get("/custom-exc", headers=headers)
    assert json.loads(resp.content) == {"exception": "handled"}
    assert (
        resp.headers.get(HeaderKeys.request_id)
        == headers[HeaderKeys.request_id]
    )
