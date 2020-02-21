from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from starlette_context.middleware import ContextMiddleware

from starlette_context import plugins, context


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


app = Starlette()
app.add_middleware(
    GetPayloadFromBodyMiddleware.with_plugins(GetPayloadUsingPlugin)
)


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

    # ugly cleanup
    ContextMiddleware.plugins = []
