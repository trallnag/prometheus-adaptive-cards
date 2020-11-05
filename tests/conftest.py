import logging

import pytest
from _pytest.logging import caplog as _caplog
from loguru import logger
from prettyprinter import cpprint

from prometheus_adaptive_cards.config.logger import setup_logging
from prometheus_adaptive_cards.config.settings import Logging


class Helpers:
    @staticmethod
    def print_struct(structure, description: str = "No description:") -> None:
        print(f"\n{description}")
        cpprint(structure)
        print("")


@pytest.fixture
def helpers():
    return Helpers


@pytest.fixture(scope="session", autouse=True)
def setup_logging_for_pytest():
    setup_logging(logging_settings=Logging(level="DEBUG", format="unstructured"))


@pytest.fixture
def caplog(_caplog):
    class PropogateHandler(logging.Handler):
        def emit(self, record):
            logging.getLogger(record.name).handle(record)

    handler_id = logger.add(PropogateHandler(), format="{message} {extra}")
    yield _caplog
    logger.remove(handler_id)
