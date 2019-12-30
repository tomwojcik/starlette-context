from contextvars import ContextVar


_request_scope_context_storage: ContextVar[str] = ContextVar(
    "starlette_context"
)


from starlette_context.context import context
from starlette_context.middlewares.basic_context_middleware import BasicContextMiddleware
from starlette_context.middlewares.empty_context_middleware import EmptyContextMiddleware
