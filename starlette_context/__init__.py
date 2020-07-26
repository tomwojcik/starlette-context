from contextvars import ContextVar

__version__ = "0.2.3"
__author__ = "Tomasz Wojcik"


_request_scope_context_storage: ContextVar[str] = ContextVar(
    "starlette_context"
)

from starlette_context.ctx import context  # noqa: E402, F401
