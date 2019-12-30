from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from starlette_context import EmptyContextMiddleware


async def index(request: Request):
    from starlette_context import context
    return JSONResponse(context.dict())


class EmptyContext(EmptyContextMiddleware):
    def set_context(self, request: Request) -> dict:
        return {
            'empty_context': 'test'
        }


class AdditionalMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ):
        from starlette_context import context
        context['additional_middleware'] = 'test'
        return await call_next(request)


routes = [Route("/", index)]

app = Starlette(debug=True, routes=routes)
app.add_middleware(AdditionalMiddleware)
app.add_middleware(EmptyContext)

client = TestClient(app)


def test_response():
    response = client.get("/")
    expected = {
        'empty_context': 'test',
        'additional_middleware': 'test'
    }
    assert expected == response.json()
