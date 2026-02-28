import asyncio
import uuid

import pytest
from starlette.applications import Starlette
from starlette.background import BackgroundTask, BackgroundTasks
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from starlette_context import context, plugins
from starlette_context.header_keys import HeaderKeys
from starlette_context.middleware import (
    ContextMiddleware,
    RawContextMiddleware,
)


def make_app(middleware_cls):
    background_results = []

    async def endpoint_single(request: Request) -> JSONResponse:
        request_id = context[HeaderKeys.request_id]
        task = BackgroundTask(sync_bg_task, background_results, request_id)
        return JSONResponse({"request_id": request_id}, background=task)

    async def endpoint_async(request: Request) -> JSONResponse:
        request_id = context[HeaderKeys.request_id]
        task = BackgroundTask(async_bg_task, background_results, request_id)
        return JSONResponse({"request_id": request_id}, background=task)

    async def endpoint_multiple(request: Request) -> JSONResponse:
        request_id = context[HeaderKeys.request_id]
        tasks = BackgroundTasks()
        for i in range(3):
            tasks.add_task(sync_bg_task, background_results, request_id)
        return JSONResponse({"request_id": request_id}, background=tasks)

    app = Starlette(
        routes=[
            Route("/single", endpoint_single),
            Route("/async", endpoint_async),
            Route("/multiple", endpoint_multiple),
        ],
    )
    app.add_middleware(
        middleware_cls,
        plugins=(plugins.RequestIdPlugin(),),
    )
    return app, background_results


def sync_bg_task(results: list, expected_request_id: str) -> None:
    results.append(context[HeaderKeys.request_id])
    assert context[HeaderKeys.request_id] == expected_request_id


async def async_bg_task(results: list, expected_request_id: str) -> None:
    await asyncio.sleep(0.01)
    results.append(context[HeaderKeys.request_id])
    assert context[HeaderKeys.request_id] == expected_request_id


@pytest.fixture(params=[ContextMiddleware, RawContextMiddleware])
def app_and_results(request):
    return make_app(request.param)


def test_context_available_in_sync_background_task(app_and_results):
    app, results = app_and_results
    request_id = uuid.uuid4().hex
    with TestClient(app) as client:
        resp = client.get(
            "/single", headers={HeaderKeys.request_id: request_id}
        )
    assert resp.status_code == 200
    assert resp.json()["request_id"] == request_id
    assert results == [request_id]


def test_context_available_in_async_background_task(app_and_results):
    app, results = app_and_results
    request_id = uuid.uuid4().hex
    with TestClient(app) as client:
        resp = client.get(
            "/async", headers={HeaderKeys.request_id: request_id}
        )
    assert resp.status_code == 200
    assert resp.json()["request_id"] == request_id
    assert results == [request_id]


def test_context_available_in_multiple_background_tasks(app_and_results):
    app, results = app_and_results
    request_id = uuid.uuid4().hex
    with TestClient(app) as client:
        resp = client.get(
            "/multiple", headers={HeaderKeys.request_id: request_id}
        )
    assert resp.status_code == 200
    assert results == [request_id] * 3


def test_context_isolated_between_requests(app_and_results):
    app, results = app_and_results
    request_ids = [uuid.uuid4().hex for _ in range(5)]
    with TestClient(app) as client:
        for rid in request_ids:
            resp = client.get("/single", headers={HeaderKeys.request_id: rid})
            assert resp.status_code == 200
            assert resp.json()["request_id"] == rid
    assert results == request_ids
