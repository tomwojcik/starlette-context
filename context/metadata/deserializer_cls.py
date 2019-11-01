from starlette.datastructures import Headers, Address, QueryParams

from context.metadata.dataclass import RequestMetadataDataclass


class DefaultDeserializer:
    def __init__(self, stored_request: dict):
        self.request = stored_request

    @property
    def type(self):
        return self.request.get("type")

    @property
    def http_version(self):
        return self.request.get("http_version")

    @property
    def server(self) -> Address:
        host, port = self.request["server"]
        return Address(host=host, port=port)

    @property
    def client(self) -> Address:
        host, port = self.request["client"]
        return Address(host=host, port=port)

    @property
    def scheme(self) -> str:
        return self.request.get("scheme")

    @property
    def method(self) -> str:
        return self.request.get("method")

    @property
    def root_path(self) -> str:
        return self.request.get("root_path")

    @property
    def path(self) -> str:
        return self.request.get("path")

    @property
    def raw_path(self) -> bytes:
        return self.request.get("raw_path")

    @property
    def query_string(self) -> QueryParams:
        return QueryParams(self.request.get("query_string"))

    @property
    def headers(self) -> Headers:
        raw_headers = self.request.get("headers", [])
        if raw_headers:
            return Headers(raw=raw_headers)
        return raw_headers

    @property
    def cookies(self) -> dict:
        return self.request.get("cookies")

    def get(self) -> RequestMetadataDataclass:
        return RequestMetadataDataclass(
            type=self.type,
            http_version=self.http_version,
            server=self.server,
            client=self.client,
            scheme=self.scheme,
            method=self.method,
            root_path=self.root_path,
            query_params=self.query_string,
            path=self.path,
            raw_path=self.raw_path,
            headers=self.headers,
            cookies=self.cookies,
        )
