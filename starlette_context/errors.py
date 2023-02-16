from typing import Optional
from starlette.responses import Response


class StarletteContextError(Exception):
    pass


class ContextDoesNotExistError(RuntimeError, StarletteContextError):
    def __init__(self):
        self.message = (
            "You didn't use the required middleware or "
            "you're trying to access `context` object "
            "outside of the request-response cycle."
        )
        super().__init__(self.message)


class ConfigurationError(StarletteContextError):
    pass


class MiddleWareValidationError(StarletteContextError):
    def __init__(
        self, *args, error_response: Optional[Response] = None
    ) -> None:
        super().__init__(*args)
        self.error_response = error_response


class WrongUUIDError(MiddleWareValidationError):
    pass


class DateFormatError(MiddleWareValidationError):
    pass
