from starlette.exceptions import HTTPException
from typing import Optional
from starlette import status


class StarletteContextException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Error"

    def __init__(
        self,
        detail: Optional[str] = None,
        status_code: Optional[int] = None,
    ) -> None:
        super().__init__(
            status_code=status_code or self.status_code,
            detail=detail or self.detail,
        )


class ContextDoesNotExistError(StarletteContextException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __str__(self):  # pragma: no cover
        return (
            "You didn't use the required middleware or "
            "you're trying to access `context` object "
            "outside of the request-response cycle"
        )


class ConfigurationError(StarletteContextException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __str__(self):  # pragma: no cover
        return "Invalid starlette-context configuration"


class WrongUUIDError(StarletteContextException):
    detail = "Invalid UUID in request header"


class DateFormatError(StarletteContextException):
    detail = "Date header in wrong format, has to match rfc1123"
