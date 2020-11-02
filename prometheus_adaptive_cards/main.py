"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import os
import sys

import uvicorn
from loguru import logger

from prometheus_adaptive_cards.api.app import create_fastapi_base
from prometheus_adaptive_cards.config.logger import setup_logging
from prometheus_adaptive_cards.config.settings import settings_singleton


def main(cli_args: list[str], env: dict[str, str]):
    # Intermediate logging settings to have nice logs during settings setup.
    setup_logging()

    settings = settings_singleton(cli_args, env, refresh=True)

    # Configure logging.
    setup_logging(logging_settings=settings.logging)

    fastapi_app = create_fastapi_base()
    logger.error("Hallo")
    uvicorn.run(
        fastapi_app,
        host=settings.server.host,
        port=settings.server.port,
        log_level=str.lower(settings.logging.level),
        log_config=None,
    )


if __name__ == "__main__":
    main(cli_args=sys.argv[1:], env=dict(os.environ))
