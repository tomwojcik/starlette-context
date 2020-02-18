import pytest
from starlette.requests import Request
from starlette.responses import Response

from starlette_context import plugins
from starlette_context.header_keys import HeaderKeys
from tests.conftest import dummy_forwarded_for


@pytest.fixture(scope="function", autouse=True)
def plugin():
    return plugins.ForwardedForPlugin()


@pytest.mark.asyncio
async def test_process_request_for_existing_header(
    plugin: plugins.ForwardedForPlugin, mocked_request: Request
):
    assert dummy_forwarded_for == await plugin.process_request(mocked_request)
    assert dummy_forwarded_for == plugin.value


@pytest.mark.asyncio
async def test_process_request_for_missing_header(
    plugin: plugins.ForwardedForPlugin, mocked_request: Request
):
    del mocked_request.headers[HeaderKeys.forwarded_for]
    assert HeaderKeys.forwarded_for not in mocked_request.headers
    val = await plugin.process_request(mocked_request)
    assert val is None
    assert plugin.value is None


@pytest.mark.asyncio
async def test_enrich_response_str(
    plugin: plugins.ForwardedForPlugin,
    mocked_request: Request,
    mocked_response: Response,
):
    await plugin.process_request(mocked_request)
    await plugin.enrich_response(mocked_response)

    assert HeaderKeys.forwarded_for.lower() not in mocked_response.headers
