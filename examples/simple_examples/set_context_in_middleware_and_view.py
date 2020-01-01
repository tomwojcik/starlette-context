from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

import uvicorn
from starlette_context import EmptyContextMiddleware, context


async def index(request: Request):
    context["view"] = True
    return JSONResponse(context.dict())


class ContextFromMiddleware(EmptyContextMiddleware):
    def set_context(self, request: Request) -> dict:
        return {"middleware": True}


routes = [Route("/", index)]

app = Starlette(debug=True, routes=routes)
app.add_middleware(ContextFromMiddleware)
uvicorn.run(app, host="0.0.0.0")
