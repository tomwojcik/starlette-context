from starlette_context.plugins.base import Plugin
from typing import Any

class ForwardedForPlugin(Plugin):
    key: Any = ...
