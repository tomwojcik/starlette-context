from starlette_context.plugins.base import Plugin

class ApiKeyPlugin(Plugin):
    key: str
