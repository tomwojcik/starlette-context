from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from starlette_context import context, plugins
from starlette_context.middleware import ContextMiddleware


class GetPayloadUsingPlugin(plugins.Plugin):
    key = "from_plugin"

    async def process_request(self, request: Request) -> dict:
        self.value = await request.json()
        return self.value


class GetPayloadFromBodyMiddleware(ContextMiddleware):
    async def set_context(self, request: Request) -> dict:
        from_plugin = await super(
            GetPayloadFromBodyMiddleware, self
        ).set_context(request)
        return {"from_middleware": await request.json(), **from_plugin}


middleware = [
    Middleware(
        GetPayloadFromBodyMiddleware, plugins=(GetPayloadUsingPlugin(),)
    )
]
app = Starlette(middleware=middleware)


@app.route("/", methods=["POST"])
async def index(request: Request):
    return JSONResponse(context.data)


client = TestClient(app)


def test_async_body():
    payload = {"test": "payload"}
    resp = client.post("/", json=payload)
    expected_resp = {
        "from_middleware": {"test": "payload"},
        "from_plugin": {"test": "payload"},
    }
    assert expected_resp == resp.json()
