"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import os
import sys

from prometheus_adaptive_cards.config.settings import settings_singleton


def main(cli_args: list[str], env: dict[str, str]):
    # setup_minimal_loguru()
    settings = settings_singleton(cli_args, env, refresh=True)


if __name__ == "__main__":
    main(cli_args=sys.argv[1:], env=dict(os.environ))
