from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse

import uvicorn

import starlette_context.middleware.context_middleware
from examples.example_with_logger.logger import log
from starlette_context import context, middleware, plugins

middleware = [
    Middleware(
        starlette_context.middleware.context_middleware.ContextMiddleware,
        plugins=(
            plugins.CorrelationIdPlugin(),
            plugins.RequestIdPlugin(),
            plugins.DateHeaderPlugin(),
            plugins.ForwardedForPlugin(),
            plugins.UserAgentPlugin(),
        ),
    )
]

app = Starlette(debug=True, middleware=middleware)


@app.route("/")
async def index(_: Request):
    log.info("Log from view")
    return JSONResponse(context.data)


uvicorn.run(app, host="0.0.0.0")
