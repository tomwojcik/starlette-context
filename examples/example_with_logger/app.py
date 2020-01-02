from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse

import uvicorn
from examples.example_with_logger.logger import log
from starlette_context import context, plugins, middleware

app = Starlette(debug=True)


@app.route('/')
async def index(request: Request):
    log.info("Log from view")
    return JSONResponse(context.dict())


app.add_middleware(middleware.ContextMiddleware.with_plugins(
    plugins.CorrelationIdPlugin,
    plugins.RequestIdPlugin,
    plugins.DateHeaderPlugin,
    plugins.ForwardedForPlugin,
    plugins.UserAgentPlugin
))
uvicorn.run(app, host="0.0.0.0")
