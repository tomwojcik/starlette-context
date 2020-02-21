import pytest
from starlette.requests import Request
from starlette.responses import Response

from starlette_context import plugins
from starlette_context.header_keys import HeaderKeys
from tests.conftest import dummy_request_id


@pytest.fixture(scope="function", autouse=True)
def plugin():
    return plugins.RequestIdPlugin()


@pytest.mark.asyncio
async def test_process_request_for_existing_header(
    plugin: plugins.RequestIdPlugin, mocked_request: Request
):
    assert dummy_request_id == await plugin.process_request(mocked_request)
    assert dummy_request_id == plugin.value


@pytest.mark.asyncio
async def test_process_request_for_missing_header(
    plugin: plugins.RequestIdPlugin, mocked_request: Request
):
    del mocked_request.headers[HeaderKeys.request_id]

    assert HeaderKeys.request_id not in mocked_request.headers

    uuid1 = await plugin.process_request(mocked_request)
    assert uuid1 is not None
    assert isinstance(uuid1, str)

    uuid2 = await plugin.process_request(mocked_request)
    assert uuid2 is not None
    assert isinstance(uuid2, str)

    assert uuid1 != uuid2


@pytest.mark.asyncio
async def test_enrich_response_str(
    plugin: plugins.RequestIdPlugin,
    mocked_request: Request,
    mocked_response: Response,
):
    await plugin.process_request(mocked_request)
    await plugin.enrich_response(mocked_response)

    assert dummy_request_id == mocked_response.headers[HeaderKeys.request_id]
