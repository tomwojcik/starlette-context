from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse

import uvicorn
from starlette_context import context, plugins
from starlette_context.middleware import RawContextMiddleware

middleware = [
    Middleware(
        RawContextMiddleware,
        plugins=(plugins.RequestIdPlugin(), plugins.CorrelationIdPlugin()),
    )
]

app = Starlette(debug=True, middleware=middleware)


@app.route("/")
async def index(request: Request):
    return JSONResponse(context.data)


uvicorn.run(app, host="0.0.0.0")
