from unittest import mock

import pytest
from starlette.requests import Request
from starlette.responses import Response

from starlette_context import plugins
from starlette_context.errors import StarletteContextError


@pytest.fixture(scope="function", autouse=True)
def plugin():
    class DummyPlugin(plugins.Plugin):
        key = "key"

        async def enrich_response(self, response: Response) -> None:
            await super().enrich_response(response)

    return DummyPlugin()


@pytest.mark.asyncio
async def test_getter_for_headers(
    mocked_request: Request, plugin: plugins.Plugin
):
    key_title = "X-Test-Header"
    key_lower = key_title.lower()
    value = "test_value"

    mocked_request.headers[key_title] = value
    plugin.key = key_title
    assert value == await plugin.extract_value_from_header_by_key(
        mocked_request
    )

    mocked_request.headers[key_lower] = value
    plugin.key = key_title
    assert value == await plugin.extract_value_from_header_by_key(
        mocked_request
    )

    mocked_request.headers[key_lower] = value
    plugin.key = key_lower
    assert value == await plugin.extract_value_from_header_by_key(
        mocked_request
    )


@pytest.mark.asyncio
async def test_plugin_exceptions_handled_generically(
    mocked_request: Request, plugin: plugins.Plugin
):
    """
    Verifies that exceptions raised by plugins are caught normally.
    """
    try:
        with (
            mock.patch.object(
                plugin,
                "extract_value_from_header_by_key",
                side_effect=StarletteContextError,
            ),
            pytest.raises(Exception),
        ):
            await plugin.extract_value_from_header_by_key(mocked_request)
    except BaseException:
        pytest.fail(
            "General exceptions should subclass Exception (not BaseException)"
        )
