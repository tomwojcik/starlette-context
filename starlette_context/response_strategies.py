import abc

from starlette.datastructures import MutableHeaders
from starlette.responses import Response

from starlette_context import context

__all__ = [
    "EnrichResponseStrategy",
    "NoEnrichResponseStrategy",
    "BasicEnrichResponseStrategy",
]


class EnrichResponseStrategy(metaclass=abc.ABCMeta):
    def __init__(self, key):
        self.key = key

    @abc.abstractmethod
    async def enrich_response(self, arg) -> None:
        ...


class NoEnrichResponseStrategy(EnrichResponseStrategy):
    async def enrich_response(self, arg) -> None:
        pass


class BasicEnrichResponseStrategy(EnrichResponseStrategy):
    async def enrich_response(self, arg) -> None:
        value = context.get(self.key)

        # for ContextMiddleware
        if isinstance(arg, Response):
            arg.headers[self.key] = value
        # for ContextPureMiddleware
        else:
            headers = MutableHeaders(scope=arg)
            headers.append(self.key, value)
