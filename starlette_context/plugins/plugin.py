import abc
from typing import Optional, Union

from starlette.requests import Request
from starlette.responses import Response


class Plugin(metaclass=abc.ABCMeta):
    key: str = None
    add_to_response: bool = False

    instantiated = False

    def __init__(self):
        Plugin.instantiated = True
        self.value = None

    def get_from_header_by_key(self, request: Request) -> Optional[str]:
        # http/2 headers lowercase
        if self.key != self.key.lower():
            self.value = request.headers.get(self.key) or request.headers.get(
                self.key.lower()
            )
        else:
            self.value = request.headers.get(self.key)

        return self.value

    def process_request(self, request: Request) -> Union[str, int]:
        assert isinstance(self.key, str)
        return self.get_from_header_by_key(request)

    def enrich_response(self, response: Response) -> None:
        if self.add_to_response:
            if isinstance(self.value, int):
                response.headers[self.key] = str(self.value)
            elif isinstance(self.value, str):
                response.headers[self.key] = self.value
            else:
                raise TypeError(
                    f"Can't assign header of type {type(self.value)}"
                )
