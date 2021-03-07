from starlette_context.plugins.base import Plugin
from typing import Any

class ApiKeyPlugin(Plugin):
    key: Any = ...
