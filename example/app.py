from typing import Union

from starlette import status
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.requests import HTTPConnection, Request
from starlette.responses import HTMLResponse, JSONResponse, Response

import structlog

from starlette_context import context
from starlette_context.middleware import RawContextMiddleware


class ContextFromMiddleware(RawContextMiddleware):
    async def set_context(self, request: Union[Request, HTTPConnection]) -> dict:
        return {'from_middleware': True}


middlewares = [
    Middleware(ContextFromMiddleware)
]


app = Starlette(debug=True, middleware=middlewares)
logger = structlog.get_logger("starlette_context_example")


@app.on_event("startup")
async def startup_event() -> None:
    from setup_logging import setup_logging
    setup_logging()


@app.route('/from-middleware')
async def example1(request: Request):
    await logger.info('log from example1 view')
    return JSONResponse(context.data)


@app.route('/from-view')
async def example2(request: Request):
    await logger.info('log from example2 view')
    context['from_view'] = True
    return JSONResponse(context.data)


@app.route("/")
async def index(request: Request):
    url = request.base_url

    await logger.info('log from index view')
    return HTMLResponse(f"<html>"
                        f"<body>"
                        f"<h1>Example usages of starlette-context</h1>"
                        f"<a href={url}from-middleware>Example 1</a> - set context in middleware"
                        f"<br>"
                        f"<a href={url}from-view>Example 2</a> - change context in view"
                        f"<br>"
                        f"<a href={url}error>Example 3</a> - handle exception logger"
                        f"</body>"
                        f"</html>"
                        f"")
