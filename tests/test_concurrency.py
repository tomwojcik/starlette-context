import uuid

import httpx

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from starlette_context import context, plugins
from starlette_context.header_keys import HeaderKeys
from starlette_context.middleware import RawContextMiddleware
import pytest
import pytest_asyncio
from starlette.routing import Route
from asgi_lifespan import LifespanManager
from starlette.exceptions import HTTPException


def should_raise(number: int) -> bool:
    return number % 2 == 0


@pytest_asyncio.fixture
async def app():
    class CloudProviderException(HTTPException):
        pass

    async def cloud_provider_exception_handler(
        request: Request, exc: HTTPException
    ):
        return JSONResponse(
            {"detail": exc.detail},
            status_code=exc.status_code,
            headers={HeaderKeys.request_id: context[HeaderKeys.request_id]},
        )

    async def index(request: Request) -> JSONResponse:
        number = request.path_params["number"]
        if should_raise(number):
            raise CloudProviderException
        return JSONResponse(
            content={
                "trace_id": context[HeaderKeys.request_id],
                "from": "view",
            }
        )

    middleware = [
        Middleware(
            RawContextMiddleware,
            plugins=(plugins.RequestIdPlugin(),),
        )
    ]
    exception_handlers = {
        CloudProviderException: cloud_provider_exception_handler
    }
    app = Starlette(
        middleware=middleware,
        routes=[Route("/{number:int}", index)],
        exception_handlers=exception_handlers,
    )

    async with LifespanManager(app):
        yield app


@pytest.mark.asyncio
async def test_concurrency_correct_headers(app):
    transport = httpx.ASGITransport(app=app, raise_app_exceptions=False)
    async with httpx.AsyncClient(
        app=app, transport=transport, base_url="http://test"
    ) as client:
        for number in range(1, 101):
            rid = uuid.uuid4().hex
            resp = await client.get(
                f"/{number}", headers={HeaderKeys.request_id: rid}
            )

            if should_raise(number):
                assert resp.status_code == 500
                assert resp.headers[HeaderKeys.request_id] == rid
            else:
                assert resp.status_code == 200
                d = resp.json()
                assert d["from"] == "view"
                assert d["trace_id"] == rid
                assert resp.headers[HeaderKeys.request_id] == rid
