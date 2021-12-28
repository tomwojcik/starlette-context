from starlette.exceptions import HTTPException
from typing import Optional
from starlette import status


class StarletteContextServerException(BaseException):
    """Results in 500 error."""

    ...


class StarletteContextClientException(HTTPException):
    """Results in 4xx errors."""

    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(
        self,
        detail: Optional[str] = None,
        status_code: Optional[int] = None,
    ) -> None:
        super().__init__(
            status_code=status_code or self.status_code,
            detail=detail or self.detail,
        )


class ContextDoesNotExistError(StarletteContextServerException):
    def __str__(self):  # pragma: no cover
        return (
            "You didn't use the required middleware or "
            "you're trying to access `context` object "
            "outside of the request-response cycle."
        )


class ConfigurationError(StarletteContextServerException):
    def __str__(self):  # pragma: no cover
        return "Invalid starlette-context configuration"


class WrongUUIDError(StarletteContextClientException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Invalid UUID in request header"


class DateFormatError(StarletteContextClientException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Date header in wrong format, has to match rfc1123."
