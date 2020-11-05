"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import copy
from typing import Any, Literal

from loguru import logger


def group_alerts(
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
            logger.bind(alert=alert).debug(f"'{group_by}' not found in alert {target}.")
            alerts_without_target.append(alert)

    return [alerts_without_target] + list(alerts_grouped_by_value.values())

