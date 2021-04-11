from starlette_context.plugins.base import PluginUUIDBase

class RequestIdPlugin(PluginUUIDBase):
    key: str
