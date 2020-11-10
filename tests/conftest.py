import sys

import pytest
from loguru import logger
from prettyprinter import cpprint

# ==============================================================================


class Helpers:
    @staticmethod
    def print_struct(structure, description: str = "No description:") -> None:
        print(f"\n{description}")
        cpprint(structure)
        print("")


@pytest.fixture
def helpers():
    return Helpers


# ==============================================================================


@pytest.fixture(scope="session", autouse=True)
def setup_logging_for_pytest():
    logger.remove()
    logger.add(
        sys.stderr,
        level="DEBUG",
        colorize=True,
        format=r"<level>{level}</level> <cyan>{module}:{function}:{line}</cyan> {message} <dim>{extra}</dim>",
    )
