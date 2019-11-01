from requests import Request

from context.custom.middleware import PreserveCustomContextMiddleware


class PreserveIdentifiersMiddleware(PreserveCustomContextMiddleware):
    def set_context(self, request: Request) -> dict:
        return {
            "correlation_id": self.get_correlation_id(request),
            "request_id": self.get_request_id(request),
        }
