from collections import UserDict
from contextvars import copy_context
from typing import Any

from starlette_context import _request_scope_context_storage


class _Context(UserDict):
    """
    A mapping with dict-like interface.
    It is using request context as a data store.
    Can be used only if context has been created in the middleware.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        # not calling super on purpose
        if args or kwargs:
            raise AttributeError("Can't instantiate with attributes")

    @property
    def data(self) -> dict:  # type: ignore
        """
        Dump this to json. Object itself it not serializable.
        """
        try:
            return _request_scope_context_storage.get()
        except LookupError as e:
            raise RuntimeError(
                "You didn't use ContextMiddleware or "
                "you're trying to access `context` object "
                "outside of the request-response cycle."
            ) from e

    def exists(self) -> bool:
        return _request_scope_context_storage in copy_context()

    def copy(self) -> dict:  # type: ignore
        """
        Read only context data.
        """
        import copy

        return copy.copy(self.data)


context = _Context()
