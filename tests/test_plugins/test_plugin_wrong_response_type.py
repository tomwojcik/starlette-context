import pytest
from starlette import status
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.testclient import TestClient

from tests.conftest import dummy_correlation_id

from starlette_context.header_keys import HeaderKeys
from starlette_context.middleware import ContextMiddleware
from starlette_context import plugins
from typing import Any


class BrokenCorrelationIdPlugin(plugins.CorrelationIdPlugin):
    def get_new_uuid(self) -> Any:
        func = self.uuid_functions_mapper[self.version]
        return func()


middleware = [
    Middleware(
        ContextMiddleware,
        plugins=(
            BrokenCorrelationIdPlugin(force_new_uuid=True, validate=False),
        ),
    )
]
app = Starlette(middleware=middleware)
client = TestClient(app)


@app.route("/")
async def index(request: Request) -> Response:
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def test_valid_request_returns_proper_response():
    with pytest.raises(TypeError):
        client.get("/")

    allow_500_client = TestClient(app, raise_server_exceptions=False)
    response = allow_500_client.get("/")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
