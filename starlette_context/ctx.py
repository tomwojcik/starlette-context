from collections import UserDict
from typing import Any

from starlette_context import _request_scope_context_storage


class _Context(UserDict):
    """
    A mapping with dict-like interface.
    It is using request context as a data store.
    Can be used only if context has been created in the middleware.

    If you know Flask, it can be compared to g object.
    """

    def __init__(self, *args: Any, **kwargs: Any):
        # not calling super on purpose
        if args or kwargs:
            raise AttributeError("Can't instantiate with attributes")

    @property
    def data(self) -> dict:
        """
        Dump this to json. Object itself it not serializable.
        """
        return _request_scope_context_storage.get()

    def copy(self) -> dict:
        """
        Read only context data.
        """
        import copy

        return copy.copy(self.data)


context = _Context()
