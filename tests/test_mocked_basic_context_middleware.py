import datetime

import pytest
from starlette.requests import Request

from starlette_context import BasicContextMiddleware
from starlette_context.header_contants import HeaderConstants
from tests.conftest import (
    dummy_correlation_id,
    dummy_forwarded_for,
    dummy_request_id,
    dummy_user_agent,
)


def test_set_context_method(
    mocked_request: Request,
    mocked_middleware: BasicContextMiddleware,
    headers: dict,
):
    expected_response = headers.copy()
    rfc1123_date = expected_response[HeaderConstants.date][:25]
    expected_response[
        HeaderConstants.date
    ] = BasicContextMiddleware.rfc1123_to_dt(rfc1123_date)
    assert expected_response == mocked_middleware.set_context(mocked_request)


def test_get_forwarded_for(
    mocked_request: Request, mocked_middleware: BasicContextMiddleware,
):
    assert dummy_forwarded_for == mocked_middleware.get_forwarded_for(
        mocked_request
    )


@pytest.mark.parametrize(
    "date_header",
    [
        "Wed, 01 Jan 2020 04:27:12 PM CET",
        "Wed, 01 Jan 2020 04:27:12 PM GMT",
        "Wed, 01 Jan 2020 04:27:12 PM GMT-4",
        "invalid",
    ],
)
def test_invalid_dates(
    date_header: str,
    mocked_request: Request,
    mocked_middleware: BasicContextMiddleware,
):
    mocked_request.headers[HeaderConstants.date] = date_header
    with pytest.raises(ValueError):
        mocked_middleware.get_date(mocked_request)


@pytest.mark.parametrize(
    "date_header",
    [
        "Wed, 01 Jan 2020 04:27:12 GMT",
        "Wed, 01 Jan 2020 04:27:12 ",
        "Wed, 01 Jan 2020 04:27:12",
    ],
)
def test_valid_dt_dates(
    date_header: str,
    mocked_request: Request,
    mocked_middleware: BasicContextMiddleware,
):
    mocked_request.headers[HeaderConstants.date] = date_header
    resp = mocked_middleware.get_date(mocked_request)
    assert isinstance(resp, datetime.datetime)


@pytest.mark.parametrize(
    "date_header",
    [
        "",
        None
    ],
)
def test_valid_null_dates(
    date_header: str,
    mocked_request: Request,
    mocked_middleware: BasicContextMiddleware,
):
    mocked_request.headers[HeaderConstants.date] = date_header
    resp = mocked_middleware.get_date(mocked_request)
    assert resp is None


def test_user_agent(
    mocked_request: Request, mocked_middleware: BasicContextMiddleware
):
    assert dummy_user_agent == mocked_middleware.get_user_agent(mocked_request)


def test_correlation_id(
    mocked_request: Request, mocked_middleware: BasicContextMiddleware
):
    assert dummy_correlation_id == mocked_middleware.get_correlation_id(
        mocked_request
    )


def test_request_id(
    mocked_request: Request, mocked_middleware: BasicContextMiddleware
):
    assert dummy_request_id == mocked_middleware.get_request_id(mocked_request)


def test_getter_for_headers(
    mocked_request: Request, mocked_middleware: BasicContextMiddleware
):
    key_title = "X-Test-Header"
    key_lower = key_title.lower()
    value = 1337

    mocked_request.headers[key_title] = value
    assert value == mocked_middleware.get_from_header_by_key(
        mocked_request, key_title
    )

    mocked_request.headers[key_lower] = value
    assert value == mocked_middleware.get_from_header_by_key(
        mocked_request, key_title
    )

    mocked_request.headers[key_lower] = value
    assert value == mocked_middleware.get_from_header_by_key(
        mocked_request, key_lower
    )
