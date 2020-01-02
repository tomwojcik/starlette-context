import pytest
from starlette.requests import Request
from starlette.responses import Response

from starlette_context import plugins
from starlette_context.header_keys import HeaderKeys
from tests.conftest import dummy_user_agent


@pytest.fixture(scope="function", autouse=True)
def plugin():
    return plugins.UserAgentPlugin()


def test_process_request_for_existing_header(
    plugin: plugins.UserAgentPlugin, mocked_request: Request
):
    assert dummy_user_agent == plugin.process_request(mocked_request)
    assert dummy_user_agent == plugin.value


def test_process_request_for_missing_header(
    plugin: plugins.UserAgentPlugin, mocked_request: Request
):
    del mocked_request.headers[HeaderKeys.user_agent]
    assert HeaderKeys.user_agent not in mocked_request.headers
    val = plugin.process_request(mocked_request)
    assert val is None
    assert plugin.value is None


def test_enrich_response_str(
    plugin: plugins.UserAgentPlugin,
    mocked_request: Request,
    mocked_response: Response,
):
    plugin.process_request(mocked_request)
    plugin.enrich_response(mocked_response)

    assert HeaderKeys.user_agent.lower() not in mocked_response.headers
