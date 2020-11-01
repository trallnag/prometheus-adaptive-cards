"""
Copyright 2020 Tim Schwenke. Licensed under the Apache License 2.0

Configures Loguru by adding sinks and makes everything ready to be used for
logging with FastAPI and Uvicorn. Opinionated. Importing alone is not enough.
"""

import json
import logging
import sys

import uvicorn
from loguru import logger

from prometheus_adaptive_cards.config.settings import Logging


class _InterceptHandler(logging.Handler):
    """Handler that redirects all logs to Loguru.

    **License and Attributions:** Unlicensed. All attributions go to Timothée
    Mazzucotelli. Found [here](https://pawamoy.github.io/posts/unify-logging-for-a-gunicorn-uvicorn-app/).
    """

    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def _sink(message) -> None:
    """Serializes record given by Loguru.

    Used instead of `serialize=True` to customize the contents of the
    structured log. Simplifying it for later usage in log monitoring. Also
    compare this function with
    <https://github.com/Delgan/loguru/blob/a9a2438a1ad63f41741a3c50f2efdeff17745396/loguru/_handler.py#L222>.
    """

    record = message.record

    exception = record["exception"]

    if exception is not None:
        exception = {
            "type": None if exception.type is None else exception.type.__name__,
            "value": exception.value,
            "traceback": bool(record["exception"].traceback),
        }

    print(
        json.dumps(
            {
                "timestamp": record["time"].timestamp(),
                "time": record["time"],
                "level": record["level"].name,
                "level_value": record["level"].no,
                "message": record["message"],
                "extra": record["extra"],
                "exception": exception,
                "line": record["line"],
                "module": record["module"],
                "name": record["name"],
                "function": record["function"],
                "file_name": record["file"].name,
                "file_path": record["file"].path,
                "process_id": record["process"].id,
                "thread_id": record["thread"].id,
                "elapsed_seconds": record["elapsed"].total_seconds(),
            },
            default=str,
        )
        + "\n",
        file=sys.stderr,
    )


def _setup_sink(
    format: str,
    level: str,
    structured_custom_serializer: bool,
    unstructured_fmt: str,
    unstructured_colorize: bool,
) -> int:
    """
    Adds and configures the sink Loguru should use. The default sink is removed.

    Returns:
        int: Handler / Sink id. Can be passed to `remove()`.
    """

    # Remove default handler
    logger.remove()

    if format == "structured":
        if structured_custom_serializer:
            return logger.add(_sink, format="{message}", level=level)
        else:
            return logger.add(sys.stderr, format="{message}", serialize=True, level=level)
    else:
        return logger.add(
            sys.stderr,
            colorize=unstructured_colorize,
            format=unstructured_fmt,
            level=level,
        )


def setup_logging(logging_settings: Logging = Logging()):
    """Sets up logging.

    Configures Loguru sink based on given settings and also python logging
    module default handlers and prepares Uvicorn to log to these handlers.

    Args:
        logging_settings (Logging, optional): Settings. Defaults to Logging().
    """

    _setup_sink(
        logging_settings.format,
        logging_settings.level,
        logging_settings.structured.custom_serializer,
        logging_settings.unstructured.fmt,
        logging_settings.unstructured.colorize,
    )

    logging.basicConfig(
        level=logging.getLevelName(logging_settings.level),
        handlers=[_InterceptHandler()],
    )

    uvicorn.main.LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "loggers": {
            "uvicorn": {"level": logging_settings.level},
            "uvicorn.error": {"level": logging_settings.level},
            "uvicorn.access": {"level": logging_settings.level},
        },
    }
