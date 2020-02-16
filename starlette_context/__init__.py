from contextvars import ContextVar

_request_scope_context_storage: ContextVar[str] = ContextVar(
    "starlette_context"
)

from starlette_context.ctx import context  # noqa: E402, F401
