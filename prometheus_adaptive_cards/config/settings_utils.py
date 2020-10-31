"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import copy
import os

from box import Box
from box.exceptions import BoxError, BoxKeyError
from loguru import logger

# ==============================================================================
# Stuff for config files


def merge(target: dict, source: dict or list[dict]) -> None:  # noqa: C901
    """Deep merge `source` into `target`.

    For each k,v in source: if k doesn't exist in target, it is deep copied from
    source to target. Otherwise, if v is a list, target[k] is extended with
    source[k]. If v is a set, target[k] is updated with v, If v is a dict,
    recursively deep-update it.

    Licensing and attribution: Found [here](https://www.electricmonk.nl/log/2017/05/07/merging-two-python-dictionaries-by-deep-updating/).
    Released under the MIT license. All attributions go to Ferry Boender, <ferry.boender@gmail.com>.
    Modified structure, but logic is the same.

    Args:
        target (dict): Will be updated in-place.
        source (dict or list[dict]): Will not be changed.
    """

    def inner_merge(target: dict, source: dict) -> None:
        for k, v in source.items():
            if type(v) == list:
                if k not in target:
                    target[k] = copy.deepcopy(v)
                else:
                    target[k].extend(v)
            elif type(v) == dict:
                if k not in target:
                    target[k] = copy.deepcopy(v)
                else:
                    merge(target[k], v)
            elif type(v) == set:
                if k not in target:
                    target[k] = v.copy()
                else:
                    target[k].update(v.copy())
            else:
                target[k] = copy.copy(v)

    if isinstance(source, dict):
        inner_merge(target, source)
    else:
        for element in source:
            inner_merge(target, element)


def parse_yamls(file_paths: list[str]) -> list[dict]:
    """Parses a list of YAML files into dicts.

    Args:
        file_paths (list[str]):
            List of paths to YAML files. Non-existing files will be skipped.

    Returns:
        list[dict]: Parsed content of given YAML files.
    """

    dicts = []
    for path in file_paths:
        if os.path.isfile(path):
            dicts.append(Box.from_yaml(filename=path).to_dict())
    return dicts


def generate_locations(file_paths: list[str]) -> list[str]:
    """
    Add `.local.` versions of all given strings if is file.


    Args:
        file_paths (list[str]):
            List of file paths. Every one is checked if it is a file.

    Returns:
        list[str]:
            New list that contains only valid paths to files up to the first
            `.local.` file. If not a single file has been found empty list will
            be returned.
    """

    new_list = []
    for path in file_paths:
        if os.path.isfile(path):
            new_list.append(path)
            last_dot = path.rfind(".")
            if last_dot != -1:
                local_version = path[:last_dot] + ".local." + path[last_dot + 1 :]
                if os.path.isfile(local_version):
                    new_list.append(local_version)
                    break
    return new_list


# ==============================================================================
# Stuff for env vars and cli args


def unflatten(d: dict) -> dict:
    """Convert any keys containing dotted paths to nested dicts

    Licensing and attribution: Found [here](https://stackoverflow.com/a/55545369/7391331).
    Released under the CC BY-SA 4.0 license. All attributions go to [they4kman](https://stackoverflow.com/users/148585/they4kman).
    """

    base = {}

    for key, value in d.items():
        root = base

        if "." in key:
            *parts, key = key.split(".")
            for part in parts:
                root.setdefault(part, {})
                root = root[part]

        root[key] = value

    return base


def cast(box: Box, dotted: str, target_type: type) -> None:
    """Cast given element to given type.

    Args:
        box (Box): Nested box that will be accessed with `dotted` notation.
        dotted (str): Dotted notation of field locations.
        target_type (type): Generally only `str`, `int`, `float`, or `boolean`.

    Raises:
        ValueError: [description]
    """
    try:
        value = box[dotted]
        if target_type is bool:
            if value == "True" or value == "true":
                box[dotted] = True
            else:
                box[dotted] = False
        else:
            box[dotted] = target_type(value)
    except (BoxKeyError, BoxError, TypeError):
        logger.debug(f"{dotted} not in given box.")
    except ValueError as e:
        logger.opt(exception=True).error(f"{dotted} cast to {target_type} failed.")
        raise ValueError(f"{dotted} cast to {target_type} failed.") from e


# ==============================================================================
