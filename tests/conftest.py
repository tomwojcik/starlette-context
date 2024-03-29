import functools
import uuid
from unittest.mock import MagicMock

import pytest
from starlette.datastructures import MutableHeaders
from starlette.requests import Request
from starlette.responses import Response
from starlette.testclient import TestClient

from starlette_context.header_keys import HeaderKeys
from starlette_context.middleware import ContextMiddleware

dummy_api_key = "abcdef12345"
dummy_correlation_id = uuid.uuid4().hex
dummy_request_id = uuid.uuid4().hex
dummy_user_agent = "dummy_user_agent"
dummy_date = "Wed, 01 Jan 2020 04:27:12 GMT"
dummy_forwarded_for = "203.0.113.19"


@pytest.fixture(scope="function", autouse=True)
def headers():
    h = MutableHeaders()
    h.update(
        {
            HeaderKeys.api_key: dummy_api_key,
            HeaderKeys.correlation_id: dummy_correlation_id,
            HeaderKeys.request_id: dummy_request_id,
            HeaderKeys.date: dummy_date,
            HeaderKeys.user_agent: dummy_user_agent,
            HeaderKeys.forwarded_for: dummy_forwarded_for,
        }
    )
    return h


@pytest.fixture(scope="function", autouse=True)
def mocked_middleware() -> ContextMiddleware:
    return ContextMiddleware(app=MagicMock())


@pytest.fixture(scope="function", autouse=True)
def mocked_request(headers) -> Request:
    mocked = MagicMock(spec=Request)
    mocked.headers = headers
    return mocked


@pytest.fixture(scope="function", autouse=True)
def mocked_response() -> Response:
    mock = MagicMock(spec=Response)
    mock.headers = MutableHeaders()
    return mock


@pytest.fixture
def test_client_factory():
    """See https://github.com/encode/starlette/blob/master/tests/conftest.py.
    Otherwise testing middlewares init is a pain.

    Needed after https://github.com/encode/starlette/pull/2017
    """
    return functools.partial(
        TestClient,
        backend="asyncio",
    )
