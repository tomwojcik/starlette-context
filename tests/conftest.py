from unittest.mock import MagicMock

import pytest
from starlette.requests import Request

from starlette_context import BasicContextMiddleware
from starlette_context.header_contants import HeaderConstants

dummy_correlation_id = "dummy_correlation_id"
dummy_request_id = "dummy_request_id"
dummy_user_agent = "dummy_user_agent"
dummy_date = "Wed, 01 Jan 2020 04:27:12 GMT"
dummy_forwarded_for = "203.0.113.19"


@pytest.fixture(scope="function", autouse=True)
def headers():
    return {
        HeaderConstants.cid: dummy_correlation_id,
        HeaderConstants.rid: dummy_request_id,
        HeaderConstants.date: dummy_date,
        HeaderConstants.ua: dummy_user_agent,
        HeaderConstants.forwarded_for: dummy_forwarded_for,
    }


@pytest.fixture(scope="function", autouse=True)
def mocked_middleware() -> BasicContextMiddleware:
    return BasicContextMiddleware(MagicMock())


@pytest.fixture(scope="function", autouse=True)
def mocked_request(headers) -> Request:
    mocked = MagicMock(spec=Request)
    mocked.headers = headers
    return mocked
