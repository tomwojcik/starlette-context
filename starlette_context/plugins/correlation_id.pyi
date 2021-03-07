from starlette_context.plugins.base import PluginUUIDBase

class CorrelationIdPlugin(PluginUUIDBase):
    key: str
