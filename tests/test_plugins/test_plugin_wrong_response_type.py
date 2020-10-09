import pytest
from starlette import status
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.testclient import TestClient

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
