import pytest
from prettyprinter import cpprint


class Helpers:
    @staticmethod
    def print_struct(structure, description: str = "No description:") -> None:
        print(f"\n{description}")
        cpprint(structure)
        print("")


@pytest.fixture
def helpers():
    return Helpers
