"""
Module made to merge and process all configs for PromAC into a single nested
dictionary. Ready to be injected into the settings models that PromAC uses.

Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0
"""

import os

from box import Box
from loguru import logger

import prometheus_adaptive_cards.config.settings_utils as settings_utils


def _parse_args(args: list[str]) -> Box:
    """Parses arguments into nested dict.

    Args:
        args (list[str]):
            List of all arguments passed to program. Use it like this:
            `parse_args(sys.argv[1:])`. Args must start with one or two dashes
            and only contain lower case chars, period and underscores.

    Returns:
        Box:
            Lowercased. Box instead of dict. Already nested. Can be used just
            like a dictionary. Read more [here](https://github.com/cdgriffith/Box).
            Type casting is NOT done here. `box_dots` is `True`.
    """

    if len(args) % 2 != 0:
        raise ValueError("Number of args must be not odd.")

    names, values = args[::2], args[1::2]

    cli_args_dict = {}

    for idx in range(len(names)):
        name = names[idx]
        value = values[idx]
        if name.startswith("--"):
            cli_args_dict[name[2:]] = value
        elif name.startswith("-"):
            cli_args_dict[name[1:]] = value

    return Box(settings_utils.unflatten(cli_args_dict), box_dots=True)


def _parse_files(
    force_file: str or None = None, lookup_override: list[str] or None = None
) -> dict[str]:
    """Parses config from files and merges them together.

    Args:
        force_file (str or None, optional):
            If set, this location will be the only one checked (in addition to
            `.local.`). Should point to arg from CLI or env var. Defaults to `None`.
        lookup_override (list[str] or None, optional):
            If set, the given list of locations will be used to look for files
            instead of the included one. Should generally only be necessary
            during unit testing. Defaults to `None`.

    Returns:
        dict[str]: Represents the merged version of all found YAML files. If no
            files have been parsed the returned `dict` will be empty.
    """

    if force_file:
        locations = settings_utils.generate_locations([force_file])
    else:
        locations = settings_utils.generate_locations(
            lookup_override
            or [
                f"{os.path.dirname(__file__)}/promac.yml",
                "/etc/promac/promac.yml",
            ]
        )

    configs = settings_utils.parse_yamls(locations)

    settings = {}

    if len(configs) > 1:
        settings = configs[0]
        settings_utils.merge(settings, configs[1:])
    elif len(configs) > 0:
        settings = configs[0]

    return settings


def _parse_env_vars(all_env_vars: dict[str, str]) -> Box:
    """Extracts and transforms given dict of env vars.

    Args:
        all_env_vars (dict[str, str]): Environment variables.

    Returns:
        Box:
            Lowercased. Box instead of dict. Already nested. Can be used just
            like a dictionary. Read more [here](https://github.com/cdgriffith/Box).
            Type casting is NOT done here. `box_dots` is `True`.
    """

    env_vars = {}
    for name, value in all_env_vars.items():
        if name.startswith("PROMAC__") and len(name) > 8:
            env_vars[name[8:].lower().replace("__", ".")] = value

    return Box(settings_utils.unflatten(env_vars), box_dots=True)


def _cast_vars(box: Box) -> None:
    """Casts box fields to correct type in-place. No content validation.

    Args:
        box (Box): Nested Box with `box_dots=True`.
    """

    settings_utils.cast(box, "logging.structured.custom_serializer", bool)
    settings_utils.cast(box, "logging.unstructured.colorize", bool)
    settings_utils.cast(box, "server.port", int)


def setup_raw_settings(cli_args: list[str], env: dict[str, str]) -> dict:
    """Creates one single dict that contains all settings for PromAC.

    Args:
        args (list[str]):
            List of all arguments passed to program. Use it like this:
            `parse_args(sys.argv[1:])`. Args must start with one or two dashes
            and only contain lower case chars, period and underscores.
        env (dict[str, str]): Dict with all enviornment variables.

    Returns:
        dict: Nested dictionary with all settings unvalidated.
    """
    logger.debug("Parse CLI args with argparse.")
    cli_args_box = _parse_args(cli_args)

    logger.debug("Find, parse and merge YAML config files.")
    config_file = cli_args_box.get("config_file", os.environ.get("CONFIG_FILE", None))
    collected_settings_dict = _parse_files(force_file=config_file)

    logger.debug("Extract and parse relevant env vars and merge into settings.")
    env_vars_box = _parse_env_vars(env)
    _cast_vars(env_vars_box)
    settings_utils.merge(collected_settings_dict, env_vars_box.to_dict())

    logger.debug("Extract and parse relevant CLI args")
    if cli_args_box.get("config_file"):
        del cli_args_box["config_file"]
    _cast_vars(cli_args_box)
    settings_utils.merge(collected_settings_dict, cli_args_box.to_dict())

    return collected_settings_dict
