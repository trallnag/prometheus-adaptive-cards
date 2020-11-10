"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import os
import sys

import uvicorn
from loguru import logger

from .app import create_fastapi_base, setup_routes
from .config import settings_singleton, setup_logging


def main(cli_args: list[str], env: dict[str, str]):
    setup_logging()

    settings = settings_singleton(cli_args, env, refresh=True)

    logger.remove()
    setup_logging(logging_settings=settings.logging)

    logger.bind(settings=settings.dict()).info("Running PromAC with attached settings.")

    fastapi_app = create_fastapi_base()
    setup_routes(fastapi_app, settings.routing)

    uvicorn.run(
        fastapi_app,
        host=settings.server.host,
        port=settings.server.port,
        log_level=str.lower(settings.logging.level),
        log_config=None,
    )


if __name__ == "__main__":
    main(cli_args=sys.argv[1:], env=dict(os.environ))
