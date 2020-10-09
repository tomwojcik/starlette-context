from enum import Enum


class HeaderKeys(str, Enum):
    correlation_id = "X-Correlation-ID"
    request_id = "X-Request-ID"
    date = "Date"
    forwarded_for = "X-Forwarded-For"
    user_agent = "User-Agent"
