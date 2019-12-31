import collections
from typing import Any, Iterator

from starlette_context import _request_scope_context_storage


class Context(collections.MutableMapping):
    """
    A mapping with dict-like interface.
    It is using request context as a data store.
    Can be used only if context has been created in the middleware.c
    """

    def __init__(self, *args: Any, **kwargs: Any):
        if args or kwargs:
            raise AttributeError("Can't instantiate with attributes")
        super(Context, self).__init__()

    @property
    def store(self) -> dict:
        return _request_scope_context_storage.get()  # type: ignore

    def __getitem__(self, key: str) -> Any:
        return self.store[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.store[key] = value

    def __delitem__(self, key: str) -> None:
        del self.store[key]

    def update(self, **kwargs: Any) -> None:  # type: ignore
        self.store.update(kwargs)

    def get_many(self, *args: str) -> dict:
        d = self.dict()
        return {k: d.get(k) for k in args}

    def dict(self) -> dict:
        return self.store

    def __iter__(self) -> Iterator[Any]:
        return iter(self.store)

    def __len__(self) -> int:
        return len(self.store)

    def __repr__(self) -> str:
        return f"<Context: {self.dict()}>"


context = Context()
