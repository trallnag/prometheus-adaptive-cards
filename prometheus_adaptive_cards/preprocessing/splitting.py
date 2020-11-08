"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import copy
from typing import Any, Literal

from loguru import logger

from prometheus_adaptive_cards.model import Alert, AlertGroup


def _group_alerts(
    target: Literal["annotations", "labels"], group_by: str, alerts: list[Alert]
) -> list[list[Alert]]:
    """Creates a list with lists of alerts grouped by target value.

    Args:
        target (Literal["annotations", "labels"]): What to target?
        group_by (str): Name to group by (either annotatation or label name).
        alerts (list[dict]): Alerts to group by target. Not mutated.

    Returns:
        list[list[Alert]]: A list that contains lists that contain alerts.
    """

    alerts_without_target = []
    alerts_grouped_by_value = {}

    if len(alerts) == 1:
        return [alerts]

    for alert in alerts:
        targets = alert.__dict__[target]
        if group_by in targets:
            value = targets[group_by]
            if alerts_grouped_by_value.get(value):
                alerts_grouped_by_value[value].append(alert)
            else:
                alerts_grouped_by_value[value] = [alert]
        else:
            alerts_without_target.append(alert)

    return [alerts_without_target] + list(alerts_grouped_by_value.values())


def _create_alert_group(base: AlertGroup, alerts: list[Alert]) -> AlertGroup:
    base = base.copy()
    base.alerts = alerts

    if len(alerts) > 1:
        list_of_sets_of_keys = [set(alert.annotations.keys()) for alert in alerts]
        common_keys = set.intersection(*list_of_sets_of_keys)
        for common_key in list(common_keys):
            values = {alert.annotations[common_key] for alert in alerts}
            if len(values) > 1:
                common_keys.remove(common_key)
        base.common_annotations = {key: alerts[0].annotations[key] for key in common_keys}
    else:
        base.common_annotations = alerts[0].annotations

    if len(alerts) > 1:
        list_of_sets_of_keys = [set(alert.labels.keys()) for alert in alerts]
        common_keys = set.intersection(*list_of_sets_of_keys)
        for common_key in list(common_keys):
            values = {alert.labels[common_key] for alert in alerts}
            if len(values) > 1:
                common_keys.remove(common_key)
        base.common_labels = {key: alerts[0].labels[key] for key in common_keys}
    else:
        base.common_labels = alerts[0].labels

    for key in list(base.group_labels.keys()):
        if key not in base.common_labels:
            del base.group_labels[key]

    return base


def split(
    target: Literal["annotation", "label"], by: str, alert_group: AlertGroup
) -> list[AlertGroup]:
    grouped_alerts = _group_alerts(f"{target}s", by, alert_group.alerts)
    return [_create_alert_group(alert_group, alerts) for alerts in grouped_alerts]
