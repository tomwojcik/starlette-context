import collections
from starlette_context import _request_scope_context_storage


class Context(collections.MutableMapping):
    """
    A mapping with dict-like interface.
    It is using request context as a data store.
    Can be used only if context has been created in the middleware.c
    """

    def __init__(self, *args, **kwargs):
        if args or kwargs:
            raise AttributeError("Can't instantiate with attributes")
        super(Context, self).__init__()

    @property
    def store(self) -> dict:
        return _request_scope_context_storage.get()

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, key, value):
        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def update(self, **kwargs) -> None:
        self.store.update(kwargs)

    def dict(self):
        return self.store or {}

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __repr__(self):
        return self.store


context = Context()
