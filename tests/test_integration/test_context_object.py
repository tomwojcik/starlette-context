from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from starlette_context import context, middleware


class MiddlewareUsingContextObject(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ):
        from starlette_context import context

        context.update(a=0, b=1, c=1)
        return await call_next(request)


app = Starlette()
app.add_middleware(MiddlewareUsingContextObject)
app.add_middleware(middleware.ContextMiddleware)


@app.route("/")
async def index(request: Request):
    context.update(c=2, d=3, e=4)
    context["f"] = 5
    return JSONResponse(context.dict())


client = TestClient(app)


def test_context_update():
    resp = client.get("/")
    expected = {k: v for v, k in (enumerate("abcdef"))}
    assert expected == resp.json()
