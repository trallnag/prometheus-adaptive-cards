"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import prometheus_adaptive_cards.config.settings_utils as settings_utils
import os
import argparse


def _parse_args(args: list[str]) -> argparse.Namespace:
    """Parses arguments.
    
    Args:
        args (list[str]): 
            List of all arguments passed to program. Use it like this: 
            `parse_args(sys.argv[1:])`.

    Returns:
        argparse.Namespace: Namespace object with parsed attributes. 
    """

    parser = argparse.ArgumentParser(prog='PromAC', allow_abbrev=False)

    parser.add_argument("--config_file", type=str)
    
    return parser.parse_args(args)


def _parse_files(force_file: str or None = None, lookup_override: list[str] or None = None) -> dict[str]:
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
        locations = settings_utils.generate_locations(lookup_override or [
            f"{os.path.dirname(__file__)}/promac.yml",
            "/etc/promac/promac.yml",
        ])
        
    configs = settings_utils.parse_yamls(locations)
    
    settings = {}
    
    if len(configs) > 1:
        settings = configs[0]
        settings_utils.merge(settings, configs[1:])
    elif len(configs) > 0:
        settings = configs[0]

    return settings

    
def setup_settings(cli_args: list[str]) -> None:
    cli_args = _parse_args(cli_args)
    
    config_file = getattr(cli_args, "config_file", os.environ.get("CONFIG_FILE", None))
    settings = _parse_files(force_file=config_file)

    