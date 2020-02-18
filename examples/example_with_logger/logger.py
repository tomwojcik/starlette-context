import logging
import sys

from pythonjsonlogger import jsonlogger  # pip install python-json-logger
from starlette_context import context

global_logger = logging.getLogger("logger_test")
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

formatter = jsonlogger.JsonFormatter()

handler.setFormatter(formatter)

global_logger.addHandler(handler)


class MyApiLoggingAdapter(logging.LoggerAdapter):
    def __init__(self, logger, extra=None):
        if extra is None:
            extra = {}
        super(MyApiLoggingAdapter, self).__init__(logger, extra)

    def process(self, msg, kwargs):
        # here we are basically adding context to log
        extra = self.extra.copy()
        extra.update(context.data)

        kwargs["extra"] = extra
        return msg, kwargs


log = MyApiLoggingAdapter(global_logger)
