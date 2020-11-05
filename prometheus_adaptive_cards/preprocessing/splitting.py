"""
Contains functions that split Data into multiple Data objects. Important: All
functions in this module shall take in and return dict versions of Data. This
not only improves performance but makes it a lot easier to work with the data.

Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0
"""

import copy
from typing import Any, Literal

from loguru import logger


def _group_alerts(
    target: Literal["annotations", "labels"], group_by: str, alerts: list[dict]
) -> list[list[dict]]:
    """Creates a list with lists of alerts grouped by target value.

    Args:
        target (Literal["annotations", "labels"]): What to target?
        group_by (str): Name to group by (either annotatation or label name).
        alerts (list[dict]): Alerts to group by target. Given data is
            not mutated within this function.

    Returns:
        list[list[dict]]: A list that contains lists that contains
            alerts either grouped by target value or did not have a target.
    """

    alerts_without_target = []
    alerts_grouped_by_value = {}

    if len(alerts) == 1:
        logger.debug("Alerts contain only a single alert. skip.")
        return [alerts]

    for alert in alerts:
        targets = alert.get(target)
        if group_by in targets:
            value = targets[group_by]
            if alerts_grouped_by_value.get(value):
                alerts_grouped_by_value[value].append(alert)
            else:
                alerts_grouped_by_value[value] = [alert]
        else:
            alerts_without_target.append(alert)

    return [alerts_without_target] + list(alerts_grouped_by_value.values())


def _create_data_dict(base: dict, alerts: list[dict]) -> dict:
    """
    Creates a data dict from the given base and a list of alerts. It ensures
    that the common dicts are correct. It also updates group labels.

    Args:
        base (dict): A data dict with `alerts`, `common_annotations`
            and `common_labels` deleted or empty. Will not be mutated but deep
            copied. The copied datastructure will then be filled with the
            correct data.
        alerts (list[dict]): Alerts that will be the alerts of the returned data.

    Returns:
        dict: Data dict.
    """

    base = copy.deepcopy(base)
    base["alerts"] = alerts

    for target in ["annotations", "labels"]:
        if len(alerts) > 1:
            list_of_sets_of_keys = [set(alert[target].keys()) for alert in alerts]
            common_keys = set.intersection(*list_of_sets_of_keys)
            for common_key in list(common_keys):
                values = {alert[target][common_key] for alert in alerts}
                if len(values) > 1:
                    common_keys.remove(common_key)
            base[f"common_{target}"] = {
                key: alerts[0][target][key] for key in common_keys
            }
        else:
            base[f"common_{target}"] = alerts[0][target]

    for key in list(base["group_labels"].keys()):
        if key not in base["common_labels"]:
            del base["group_labels"][key]

    return base


def split(target: Literal["annotation", "label"], by: str, data: dict) -> list[dict]:
    """
    Splits a given data dict into multiple data dicts grouped / split by either
    a annotation or label.

    Args:
        target (Literal["annotation", "labels"]): What to target?
        by (str): Name of the target (annotation or label).
        data (dict): Valid data. Will not be mutated.

    Returns:
        list[dict[str, Any]]: List of data dicts.
    """

    grouped_alerts = _group_alerts(f"{target}s", by, data["alerts"])

    base = copy.deepcopy(data)
    del base["alerts"], base["common_annotations"], base["common_labels"]

    return [_create_data_dict(base, a) for a in grouped_alerts]
