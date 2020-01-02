from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse

import uvicorn
from starlette_context import context
from starlette_context.middleware import ContextMiddleware

app = Starlette(debug=True)


@app.route('/')
async def index(request: Request):
    context["view"] = True
    return JSONResponse(context.dict())


class ContextFromMiddleware(ContextMiddleware):
    def set_context(self, request: Request) -> dict:
        return {"middleware": True}


app.add_middleware(ContextFromMiddleware)


uvicorn.run(app, host="0.0.0.0")
