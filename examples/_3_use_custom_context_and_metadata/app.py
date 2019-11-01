from fastapi import FastAPI

from context.metadata.middleware import PreserveRequestMetadataMiddleware
from .middleware import (
    CustomContextUsingFunctionFromMiddleware,
    CustomContextUsingInheritance,
)

app = FastAPI(title="ContextAndMetadataExample")

from .api import router

app.add_middleware(PreserveRequestMetadataMiddleware)
app.add_middleware(CustomContextUsingFunctionFromMiddleware)
app.add_middleware(CustomContextUsingInheritance)

app.include_router(router)
