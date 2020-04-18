from unittest.mock import MagicMock

import pytest
from starlette.datastructures import MutableHeaders
from starlette.requests import Request
from starlette.responses import Response

from starlette_context import middleware
from starlette_context.header_keys import HeaderKeys

dummy_correlation_id = "dummy_correlation_id"
dummy_request_id = "dummy_request_id"
dummy_user_agent = "dummy_user_agent"
dummy_date = "Wed, 01 Jan 2020 04:27:12 GMT"
dummy_forwarded_for = "203.0.113.19"


@pytest.fixture(scope="function", autouse=True)
def headers():
    h = MutableHeaders()
    h.update(
        {
            HeaderKeys.correlation_id: dummy_correlation_id,
            HeaderKeys.request_id: dummy_request_id,
            HeaderKeys.date: dummy_date,
            HeaderKeys.user_agent: dummy_user_agent,
            HeaderKeys.forwarded_for: dummy_forwarded_for,
        }
    )
    return h


@pytest.fixture(scope="function", autouse=True)
def mocked_middleware() -> middleware.ContextMiddleware:
    return middleware.ContextMiddleware(app=MagicMock())


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
