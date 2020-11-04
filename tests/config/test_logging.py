"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import sys

import uvicorn
from loguru import logger

from prometheus_adaptive_cards.config.logger import _setup_sink, setup_logging


def test_loguru_sink(capsys):
    sink_id = logger.add(sys.stderr, format="{message}")
    logger.info("hello")

    _, err = capsys.readouterr()
    print(err)
    logger.remove(sink_id)

    assert "hello" in err


def test_setup_sink_with_structured_custom_logs(capsys):
    sink_id = _setup_sink(
        format="structured",
        level="INFO",
        structured_custom_serializer=True,
        unstructured_fmt="does not matter",
        unstructured_colorize=True,
    )
    logger.info("helloyyy")

    _, err = capsys.readouterr()
    print(err)
    logger.remove(sink_id)

    assert '"level": "INFO", "level_value": 20, "message": "helloyyy"' in err


def test_setup_sink_with_structured_default_logs(capsys):
    sink_id = _setup_sink(
        format="structured",
        level="INFO",
        structured_custom_serializer=False,
        unstructured_fmt="does not matter",
        unstructured_colorize=True,
    )
    logger.info("helloyyy")

    _, err = capsys.readouterr()
    print(err)
    logger.remove(sink_id)

    assert '"level": "INFO", "level_value": 20, "message": "helloyyy"' not in err


def test_setup_sink_with_unstructured_logs(capsys):
    sink_id = _setup_sink(
        format="unstructured",
        level="INFO",
        structured_custom_serializer=False,
        unstructured_fmt="<green>{time:HH:mm:ss}</green> <level>{level}</level> <cyan>{function}</cyan> {message} <dim>{extra}</dim>",
        unstructured_colorize=False,
    )
    logger.info("helloyyy")

    _, err = capsys.readouterr()
    print(err)
    logger.remove(sink_id)

    assert "INFO test_setup_sink_with_unstructured_logs helloyyy" in err


def test_custom_structured_sink_with_exception(capsys):
    def raise_and_catch():
        try:
            raise ValueError("whatever")
        except ValueError:
            logger.opt(exception=True).error("Error occurred! Oh boy")

    sink_id = _setup_sink(
        format="structured",
        level="INFO",
        structured_custom_serializer=False,
        unstructured_fmt="does not matter",
        unstructured_colorize=True,
    )
    raise_and_catch()

    _, err = capsys.readouterr()
    print(err)
    logger.remove(sink_id)

    assert (
        '"exception": {"type": "ValueError", "value": "whatever", "traceback": true}'
        in err
    )


def test_uvicorn_logging_config_override():
    assert uvicorn.config.LOGGING_CONFIG == {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(message)s",
                "use_colors": None,
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',  # noqa: E501
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "uvicorn": {"handlers": ["default"], "level": "INFO"},
            "uvicorn.error": {"level": "INFO"},
            "uvicorn.access": {
                "handlers": ["access"],
                "level": "INFO",
                "propagate": False,
            },
        },
    }, "Check the `config.py` in Uvicorn and adapt to changes. Ensure that the override is still correct."

    setup_logging()

    assert uvicorn.main.LOGGING_CONFIG == {
        "version": 1,
        "disable_existing_loggers": False,
        "loggers": {
            "uvicorn": {"level": "INFO"},
            "uvicorn.error": {"level": "INFO"},
            "uvicorn.access": {"level": "INFO"},
        },
    }
