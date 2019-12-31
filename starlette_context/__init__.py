from contextvars import ContextVar

_request_scope_context_storage: ContextVar[str] = ContextVar(
    "starlette_context"
)

from starlette_context.ctx import context  # noqa: E402, F401
from starlette_context.middlewares.basic_context_middleware import (  # noqa
    BasicContextMiddleware,
)
from starlette_context.middlewares.empty_context_middleware import (  # noqa
    EmptyContextMiddleware,
)
