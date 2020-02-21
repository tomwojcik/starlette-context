import pytest
from starlette.requests import Request
from starlette.responses import Response

from starlette_context import plugins
from starlette_context.header_keys import HeaderKeys


@pytest.fixture(scope="function", autouse=True)
def plugin():
    return plugins.DateHeaderPlugin()


@pytest.mark.parametrize(
    "date_header",
    [
        "Wed, 01 Jan 2020 04:27:12 GMT",
        "Wed, 01 Jan 2020 04:27:12 ",
        "Wed, 01 Jan 2020 04:27:12",
    ],
)
@pytest.mark.asyncio
async def test_process_request_for_existing_header(
    date_header, plugin: plugins.DateHeaderPlugin, mocked_request: Request
):
    mocked_request.headers[HeaderKeys.date] = date_header
    expected_date = plugin.rfc1123_to_dt(date_header[:25])
    assert expected_date == await plugin.process_request(mocked_request)
    assert expected_date == plugin.value


@pytest.mark.parametrize(
    "date_header", ["",],  # noqa: E231
)
@pytest.mark.asyncio
async def test_process_request_for_empty_header(
    date_header, plugin: plugins.DateHeaderPlugin, mocked_request: Request
):
    mocked_request.headers[HeaderKeys.date] = date_header
    val = await plugin.process_request(mocked_request)
    assert val is None
    assert plugin.value is None


@pytest.mark.asyncio
async def test_process_request_for_missing_header(
    plugin: plugins.DateHeaderPlugin, mocked_request: Request
):
    del mocked_request.headers[HeaderKeys.date]
    assert HeaderKeys.date not in mocked_request.headers
    val = await plugin.process_request(mocked_request)
    assert val is None
    assert plugin.value is None


@pytest.mark.parametrize(
    "date_header",
    [
        "Wed, 01 Jan 2020 04:27:12 PM CET",
        "Wed, 01 Jan 2020 04:27:12 PM GMT",
        "Wed, 01 Jan 2020 04:27:12 PM GMT-4",
        "invalid",
    ],
)
@pytest.mark.asyncio
async def test_process_request_invalid_header(
    date_header: str,
    mocked_request: Request,
    plugin: plugins.DateHeaderPlugin,
):
    mocked_request.headers[HeaderKeys.date] = date_header
    with pytest.raises(ValueError):
        await plugin.process_request(mocked_request)


@pytest.mark.asyncio
async def test_enrich_response_str(
    plugin: plugins.DateHeaderPlugin,
    mocked_request: Request,
    mocked_response: Response,
):
    await plugin.process_request(mocked_request)
    await plugin.enrich_response(mocked_response)

    assert HeaderKeys.date.lower() not in mocked_response.headers
