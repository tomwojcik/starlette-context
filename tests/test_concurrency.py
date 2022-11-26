import random
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

import asyncio


def should_raise(number: int) -> bool:
    return number % 2 == 0


async def dummy_sleep():
    for i in range(random.randint(0, 100000)):
        if i % 2 and i % 3:
            pass
    return 0


@pytest_asyncio.fixture
async def app():
    async def cloud_provider_exception_handler(
        request: Request, exc: HTTPException
    ):
        return JSONResponse(
            {"detail": "asd"},
            status_code=400,
        )

    class CloudProviderException(Exception):
        pass

    async def index(request: Request) -> JSONResponse:
        number = request.path_params["number"]

        # for some reason it's not possible to
        # await asyncio.sleep(1)
        loop = asyncio.get_running_loop()
        f1 = loop.create_task(dummy_sleep())
        await asyncio.wait([f1])

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
        for number in range(1, 501):
            rid = uuid.uuid4().hex
            resp = await client.get(
                f"/{number}", headers={HeaderKeys.request_id: rid}
            )
            # print(number)
            if should_raise(number):
                assert resp.status_code == 400
                assert resp.headers[HeaderKeys.request_id] == rid
            else:
                assert resp.status_code == 200
                assert resp.headers[HeaderKeys.request_id] == rid
