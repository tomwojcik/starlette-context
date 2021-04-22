from contextvars import ContextVar
from typing import Any, Dict

__version__ = "0.3.2"
__author__ = "Tomasz Wojcik"

_request_scope_context_storage: ContextVar[Dict[Any, Any]] = ContextVar(
    "starlette_context"
)

from starlette_context.ctx import context  # noqa: E402
