"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import copy
import os

from box import Box


def merge(target: dict, source: dict or list[dict]) -> None:
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
                if not k in target:
                    target[k] = copy.deepcopy(v)
                else:
                    target[k].extend(v)
            elif type(v) == dict:
                if not k in target:
                    target[k] = copy.deepcopy(v)
                else:
                    merge(target[k], v)
            elif type(v) == set:
                if not k in target:
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
        file_paths (list[str]): List of paths to YAML files. Non-existing files
            will be skipped / ignored without error.

    Returns:
        list[dict]: Parsed content of given YAML files.
    """

    dicts = []

    for path in file_paths:
        if os.path.isfile(path):
            dicts.append(Box.from_yaml(filename=path).to_dict())

    return dicts
