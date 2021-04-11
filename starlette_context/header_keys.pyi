from enum import Enum

class HeaderKeys(str, Enum):
    api_key: str
    correlation_id: str
    request_id: str
    date: str
    forwarded_for: str
    user_agent: str
