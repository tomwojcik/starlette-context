import pytest
from starlette.requests import Request
from starlette.responses import Response

from starlette_context import plugins
from starlette_context.header_keys import HeaderKeys
from tests.conftest import dummy_correlation_id


@pytest.fixture(scope="function", autouse=True)
def plugin():
    return plugins.CorrelationIdPlugin()


def test_process_request_for_existing_header(
    plugin: plugins.CorrelationIdPlugin, mocked_request: Request
):
    assert dummy_correlation_id == plugin.process_request(mocked_request)
    assert dummy_correlation_id == plugin.value


def test_process_request_for_missing_header(
    plugin: plugins.CorrelationIdPlugin, mocked_request: Request
):
    del mocked_request.headers[HeaderKeys.correlation_id]

    assert HeaderKeys.correlation_id not in mocked_request.headers

    uuid1 = plugin.process_request(mocked_request)
    assert uuid1 is not None
    assert isinstance(uuid1, str)

    uuid2 = plugin.process_request(mocked_request)
    assert uuid2 is not None
    assert isinstance(uuid2, str)

    assert uuid1 != uuid2


def test_enrich_response_str(
    plugin: plugins.CorrelationIdPlugin,
    mocked_request: Request,
    mocked_response: Response,
):
    plugin.process_request(mocked_request)
    plugin.enrich_response(mocked_response)

    assert (
        dummy_correlation_id
        == mocked_response.headers[HeaderKeys.correlation_id]
    )
