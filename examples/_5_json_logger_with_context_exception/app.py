from fastapi import FastAPI

from .middleware import SetRequestAndCorrelationIdInContext, ExceptionMiddleware

app = FastAPI(title="ExampleLogWithJsonOnException", debug=False)

from .api import router

# order of middlewares is important
app.add_middleware(ExceptionMiddleware)  # always topmost
app.add_middleware(SetRequestAndCorrelationIdInContext)

app.include_router(router)
