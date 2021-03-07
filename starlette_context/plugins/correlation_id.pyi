from starlette_context.plugins.base import PluginUUIDBase
from typing import Any

class CorrelationIdPlugin(PluginUUIDBase):
    key: Any = ...
