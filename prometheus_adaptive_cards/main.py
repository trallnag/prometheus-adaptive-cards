"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import os
import sys

from prometheus_adaptive_cards.config.settings import settings_singleton
from prometheus_adaptive_cards.config.logger import setup_logging


def main(cli_args: list[str], env: dict[str, str]):
    # Intermediate logging settings to have nice logs during settings setup.
    setup_logging()

    settings = settings_singleton(cli_args, env, refresh=True)
    
    # Configure logging.
    setup_logging(logging_settings=settings.logging)


if __name__ == "__main__":
    main(cli_args=sys.argv[1:], env=dict(os.environ))
