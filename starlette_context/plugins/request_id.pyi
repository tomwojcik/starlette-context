from starlette_context.plugins.base import PluginUUIDBase
from typing import Any

class RequestIdPlugin(PluginUUIDBase):
    key: Any = ...
