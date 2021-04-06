from typing import Any, MutableMapping

import structlog

from starlette_context import context


def setup_logging():
    import logging.config

    def add_app_context(logger: logging.Logger, method_name: str,
                        event_dict: MutableMapping[str, Any]) -> \
            MutableMapping[str, Any]:
        if context.exists():
            event_dict.update(context.data)
        return event_dict

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            add_app_context,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.AsyncBoundLogger,
        cache_logger_on_first_use=True,
    )

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.processors.JSONRenderer(),
            },
        },
        "handlers": {
            "json": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "json",
            },
        },
        "loggers": {
            "starlette_context_example": {
                "handlers": ["json"], "level": "INFO"
            },
        },
    }
    logging.config.dictConfig(logging_config)
