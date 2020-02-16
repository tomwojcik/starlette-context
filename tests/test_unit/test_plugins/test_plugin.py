import pytest
from starlette.requests import Request
from starlette.responses import Response

from starlette_context import plugins


@pytest.fixture(scope="function", autouse=True)
def plugin():
    class DummyPlugin(plugins.Plugin):
        add_to_response = True
        key = "key"

    return DummyPlugin()


def test_getter_for_headers(mocked_request: Request, plugin: plugins.Plugin):
    key_title = "X-Test-Header"
    key_lower = key_title.lower()
    value = "test_value"

    mocked_request.headers[key_title] = value
    plugin.key = key_title
    assert value == plugin.extract_value_from_header_by_key(mocked_request)

    mocked_request.headers[key_lower] = value
    plugin.key = key_title
    assert value == plugin.extract_value_from_header_by_key(mocked_request)

    mocked_request.headers[key_lower] = value
    plugin.key = key_lower
    assert value == plugin.extract_value_from_header_by_key(mocked_request)


def test_enrich_response_str(
    mocked_response: Response, plugin: plugins.Plugin
):
    val = "asd"
    plugin.value = val
    plugin.enrich_response(mocked_response)
    assert val == mocked_response.headers[plugin.key]


def test_enrich_response_int(
    mocked_response: Response, plugin: plugins.Plugin
):
    val = 123
    plugin.value = val
    plugin.enrich_response(mocked_response)
    assert str(val) == mocked_response.headers[plugin.key]


def test_enrich_response_invalid(
    mocked_response: Response, plugin: plugins.Plugin
):
    val = None
    plugin.value = val
    with pytest.raises(TypeError):
        plugin.enrich_response(mocked_response)
