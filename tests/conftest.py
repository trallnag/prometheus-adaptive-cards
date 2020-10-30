import pytest
import pprint


class Helpers:
    printer = pprint.PrettyPrinter(width=120)
    @staticmethod
    def pp(structure: list or dict, description: str or None = None) -> None:
        """Pretty print"""

        print(f"\n{description}")
        Helpers.printer.pprint(structure)
        print("")

Helpers.pp({"hallo": "fefef"}, "fefefeffewefw")

@pytest.fixture
def helpers():
    return Helpers
