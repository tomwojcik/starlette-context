from contextvars import ContextVar, Token
from typing import Union, Dict

from starlette.middleware.base import RequestResponseEndpoint, BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from context.metadata.dataclass import RequestMetadataDataclass
from context.metadata.deserializer_cls import DefaultDeserializer

_request_storage: ContextVar[str] = ContextVar("PreserveRequestMetadataMiddleware")


def get_raw_metadata() -> dict:
    """
    Returns everything that might be useful in the request.
    """
    return _request_storage.get()


def get_metadata() -> RequestMetadataDataclass:
    """
    Loads this dict as dataclass giving you stronger typing and handles missing values.
    """
    raw_request = get_raw_metadata()
    return DefaultDeserializer(raw_request).get()


class PreserveRequestMetadataMiddleware(BaseHTTPMiddleware):
    """
    Works as PreserveContextMiddleware. The difference is that it collects all metadata by default,
    allows for loading metadata dict as dataclass and should be used as read only.
    Both might be used in parallel.
    """

    @staticmethod
    def set_context(request: Request) -> Dict[str, Union[bytes, int, str]]:
        """
        Collects metadata from request.
        """
        return {
            "client": request.scope["client"],
            "headers": request.scope["headers"],
            "http_version": request.scope["http_version"],
            "method": request.scope["method"],
            "path": request.scope["path"],
            "query_string": request.scope["query_string"],
            "raw_path": request.scope["raw_path"],
            "root_path": request.scope["root_path"],
            "scheme": request.scope["scheme"],
            "server": request.scope["server"],
            "type": request.scope["type"],
            "cookies": request.cookies,
        }

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        token: Token = _request_storage.set(self.set_context(request))
        try:
            response = await call_next(request)
        finally:
            _request_storage.reset(token)
        return response
