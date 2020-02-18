import pytest
from starlette.requests import Request

from starlette_context import plugins
from starlette_context.header_keys import HeaderKeys
from starlette_context.middleware import ContextMiddleware


@pytest.mark.asyncio
async def test_set_context_method(
    mocked_request: Request, mocked_middleware: ContextMiddleware,
):

    mocked_middleware.plugins = [plugins.DateHeaderPlugin()]
    rfc1123_date = mocked_request.headers[HeaderKeys.date][:25]
    dt_date = plugins.DateHeaderPlugin.rfc1123_to_dt(rfc1123_date)

    assert {
        plugins.DateHeaderPlugin.key: dt_date
    } == await mocked_middleware.set_context(mocked_request)
