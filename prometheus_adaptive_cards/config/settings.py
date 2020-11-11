"""
This module turns the "raw" settings into a validated Pydantic model. These
models are also codify the configuration schema.

Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0
"""

import re
from typing import Literal, Optional, Pattern

from loguru import logger
from pydantic import AnyUrl, BaseModel, ValidationError, parse_obj_as, validator

from prometheus_adaptive_cards.config.settings_raw import setup_raw_settings

# ==============================================================================
# Logging


class Structured(BaseModel):
    custom_serializer: bool = True


class Unstructured(BaseModel):
    fmt: str = (
        "<green>{time:HH:mm:ss}</green> <level>{level}</level> "
        "<cyan>{module}:{function}:{line}</cyan> {message} <dim>{extra}</dim>"
    )
    colorize: bool = True


class Logging(BaseModel):
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    format: Literal["structured", "unstructured"] = "structured"
    structured: Structured = Structured()
    unstructured: Unstructured = Unstructured()


# ==============================================================================
# Server


class Server(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000
    root_path: str = ""


# ==============================================================================
# Routing


class Sending(BaseModel):
    retries: int = 3
    backoff_factor: float = 0.3
    handle_failure: bool = True
    fallback_url: Optional[str]


class Remove(BaseModel):
    annotations: list[str] = []
    labels: list[str] = []
    re_annotations: list[Pattern] = []
    re_labels: list[Pattern] = []


class Add(BaseModel):
    annotations: dict[str, str] = {}
    labels: dict[str, str] = {}


class Override(BaseModel):
    annotations: dict[str, str] = {}
    labels: dict[str, str] = {}


class SplitBy(BaseModel):
    target: Literal["annotation", "label"]
    value: str


_PATTERN_FOR_NAME = re.compile(r"^[a-z0-9_\-]*$")


class Target(BaseModel):
    url: Optional[AnyUrl]
    expansion_url: Optional[str]
    url_from_label: Optional[str]
    url_from_annotation: Optional[str]
    sending: Optional[Sending]


class Route(BaseModel):
    name: str
    catch: bool = True
    remove: Optional[Remove]
    add: Optional[Add]
    override: Optional[Override]
    split_by: Optional[SplitBy]
    extract_webhooks: list[str] = []
    extract_webhooks_re: list[Pattern] = []
    targets: list[Target] = []
    sending: Optional[Sending]

    @validator("name")
    def validate_name(cls, v):  # noqa
        if _PATTERN_FOR_NAME.search(v):
            return v
        else:
            raise ValidationError(r"'name' must be match regex `^[A-Za-z0-9_\-]*$`. ")


class Routing(BaseModel):
    remove: Optional[Remove]
    add: Optional[Add]
    override: Optional[Override]
    routes: list[Route] = []
    sending: Optional[Sending]

    @validator("routes")
    def validate_routes_unique(cls, v):  # noqa
        if len(v) == len({route.name for route in v}):
            return v
        else:
            logger.error("Route name validation failed.")
            raise ValidationError("Routes must have unique names.")


# ==============================================================================


class Settings(BaseModel):
    logging: Logging = Logging()
    server: Server = Server()
    routing: Routing = Routing()


# ==============================================================================


_settings = None


def _ensure_generic_route_exists(settings: Settings) -> None:
    """Adds generic route to routes if name not taken.

    Args:
        settings (Settings): Settings model.
    """
    routes = settings.routing.routes
    route_names = [route.name for route in routes]
    if "generic" in route_names:
        logger.debug("Route 'generic' already exists.")
    else:
        logger.debug("Add route 'generic' to routes.")
        routes.append(Route(name="generic"))


def settings_singleton(
    cli_args: list[str] = [], env: dict[str, str] = {}, refresh: bool = False
) -> Settings:
    """Singleton for settings model.

    Args:
        args (list[str], optional):
            List of all arguments passed to program. Use it like this:
            `parse_args(sys.argv[1:])`. Args must start with one or two dashes
            and only contain lower case chars, period and underscores. Defaults
            to `[]`.
        env (dict[str, str], optional):
            Dict with all enviornment variables. Defaults to `{}`.
        refresh (bool, optional):
            Should the singleton object settings be refreshed? Defaults to `False`.

    Returns:
        Settings: Settings object.
    """

    global _settings
    if _settings and not refresh:
        return _settings
    else:
        settings_dict = setup_raw_settings(cli_args, env)
        _settings = parse_obj_as(Settings, settings_dict)
        _ensure_generic_route_exists(_settings)
        return _settings


# ==============================================================================
