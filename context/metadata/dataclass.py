from dataclasses import dataclass

from starlette.datastructures import Headers, QueryParams, Address


@dataclass
class RequestMetadataDataclass:
    type: str
    http_version: str
    server: Address
    client: Address
    scheme: str
    method: str
    root_path: str
    path: str
    raw_path: bytes
    query_params: QueryParams
    headers: Headers
    cookies: dict
