import asyncio
import random
import uuid

import httpx
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from starlette.applications import Starlette
from starlette.background import BackgroundTask
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from starlette_context import context, plugins
from starlette_context.header_keys import HeaderKeys
from starlette_context.middleware import ContextMiddleware

reqnum_reqid_mapping = {}


async def my_background_task(number: int, request_id: str) -> None:
    await asyncio.sleep(random.uniform(0.1, 0.5))  # Simulate some async work
    assert reqnum_reqid_mapping[number] == context.get(HeaderKeys.request_id)


@pytest_asyncio.fixture
async def app():
    async def index(request: Request) -> JSONResponse:
        request_id = request.headers.get(HeaderKeys.request_id)
        number = request.path_params["number"]
        reqnum_reqid_mapping[number] = request_id
        task = BackgroundTask(
            my_background_task, number=number, request_id=request_id
        )
        return JSONResponse(
            content={
                "request_id": request_id,
            },
            background=task,
        )

    middleware = [
        Middleware(
            ContextMiddleware,
            plugins=(plugins.RequestIdPlugin(),),
        )
    ]

    app = Starlette(
        middleware=middleware,
        routes=[Route("/{number:int}", index)],
    )

    async with LifespanManager(app):
        yield app


@pytest.mark.asyncio
async def test_backgroundtask_context(app):
    transport = httpx.ASGITransport(app=app, raise_app_exceptions=False)
    async with httpx.AsyncClient(
        app=app, transport=transport, base_url="http://test"
    ) as client:

        async def make_request(number: int):
            rid = str(uuid.uuid4())
            resp = await client.get(
                f"/{number}", headers={HeaderKeys.request_id: rid}
            )
            assert resp.status_code == 200
            assert resp.json() == {
                "request_id": rid,
            }
            return resp

        # Make all requests concurrently. The request handler will map the
        # request number to the request id. The background task will verify its
        # idea of the context vars is that of the request handler and it does
        # not accidentally use the context vars of another request.
        tasks = [make_request(number) for number in range(1, 21)]
        await asyncio.gather(*tasks)
