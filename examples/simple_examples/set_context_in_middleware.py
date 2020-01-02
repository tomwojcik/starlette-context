from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse

import uvicorn
from starlette_context import context, plugins
from starlette_context.middleware import ContextMiddleware

app = Starlette(debug=True)
app.add_middleware(
    ContextMiddleware.with_plugins(
        plugins.RequestIdPlugin, plugins.CorrelationIdPlugin
    )
)


@app.route("/")
async def index(request: Request):
    return JSONResponse(context.dict())


uvicorn.run(app, host="0.0.0.0")
