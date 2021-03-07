from starlette_context.plugins.base import Plugin

class ForwardedForPlugin(Plugin):
    key: str
