import pytest
from starlette.requests import Request
from starlette_context import plugins


@pytest.fixture(scope='function', autouse=True)
def plugin():
    class DummyPlugin(plugins.Plugin): pass
    return DummyPlugin()


def test_getter_for_headers(
        mocked_request: Request,
        plugin: plugins.Plugin
):
    key_title = "X-Test-Header"
    key_lower = key_title.lower()
    value = 'test_value'

    mocked_request.headers[key_title] = value
    plugin.key = key_title
    assert value == plugin.get_from_header_by_key(mocked_request)

    mocked_request.headers[key_lower] = value
    plugin.key = key_title
    assert value == plugin.get_from_header_by_key(mocked_request)

    mocked_request.headers[key_lower] = value
    plugin.key = key_lower
    assert value == plugin.get_from_header_by_key(mocked_request)
