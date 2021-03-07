from starlette_context.plugins.base import Plugin
from typing import Any

class UserAgentPlugin(Plugin):
    key: Any = ...
