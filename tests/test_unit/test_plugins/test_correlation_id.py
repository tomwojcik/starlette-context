import pytest
from starlette.requests import Request
from starlette.responses import Response

from starlette_context import plugins
from starlette_context.header_keys import HeaderKeys
from tests.conftest import dummy_correlation_id


@pytest.fixture(scope="function", autouse=True)
def plugin():
    return plugins.CorrelationIdPlugin()


@pytest.mark.asyncio
async def test_process_request_for_existing_header(
    plugin: plugins.CorrelationIdPlugin, mocked_request: Request
):
    assert dummy_correlation_id == await plugin.process_request(mocked_request)
    assert dummy_correlation_id == plugin.value


@pytest.mark.asyncio
async def test_invalid_correlation_id_uuid(
    plugin: plugins.CorrelationIdPlugin, mocked_request: Request
):
    mocked_request.headers[HeaderKeys.correlation_id] = "invalid_uuid"
    with pytest.raises(ValueError):
        await plugin.process_request(mocked_request)


@pytest.mark.asyncio
async def test_process_request_for_missing_header(
    plugin: plugins.CorrelationIdPlugin, mocked_request: Request
):
    del mocked_request.headers[HeaderKeys.correlation_id]

    assert HeaderKeys.correlation_id not in mocked_request.headers

    uuid1 = await plugin.process_request(mocked_request)
    assert uuid1 is not None
    assert isinstance(uuid1, str)

    uuid2 = await plugin.process_request(mocked_request)
    assert uuid2 is not None
    assert isinstance(uuid2, str)

    assert uuid1 != uuid2


@pytest.mark.asyncio
async def test_enrich_response_str(
    plugin: plugins.CorrelationIdPlugin,
    mocked_request: Request,
    mocked_response: Response,
):
    await plugin.process_request(mocked_request)
    await plugin.enrich_response(mocked_response)

    assert (
        dummy_correlation_id
        == mocked_response.headers[HeaderKeys.correlation_id]
    )


def test_version_cant_map_to_function():
    with pytest.raises(TypeError):
        plugins.CorrelationIdPlugin(version=123)


@pytest.mark.asyncio
async def test_force_new_uuid(
    plugin: plugins.CorrelationIdPlugin,
    mocked_request: Request,
    mocked_response: Response,
):
    plugin.force_new_uuid = True
    await plugin.process_request(mocked_request)
    await plugin.enrich_response(mocked_response)

    assert (
        dummy_correlation_id
        != mocked_response.headers[HeaderKeys.correlation_id]
    )


@pytest.mark.asyncio
async def test_uuid_validation(
    plugin: plugins.CorrelationIdPlugin,
    mocked_request: Request,
    mocked_response: Response,
):
    mocked_request.headers[HeaderKeys.correlation_id] = "invalid_uuid"
    with pytest.raises(ValueError):
        await plugin.process_request(mocked_request)
