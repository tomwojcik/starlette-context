from starlette_context.header_keys import HeaderKeys
from starlette_context.plugins.plugin import Plugin


class ForwardedForPlugin(Plugin):
    key = HeaderKeys.forwarded_for
