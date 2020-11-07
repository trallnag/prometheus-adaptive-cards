"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""


def convert_to_snake_case(data: dict) -> None:
    """Converts Alertmanager payload attributes to snake case.

    Args:
        data (dict): Alertmanager payload dict.
    """

    data["external_url"] = data["externalURL"]
    data["group_key"] = data["groupKey"]
    data["truncated_alerts"] = data["truncatedAlerts"]
    data["group_labels"] = data["groupLabels"]
    data["common_labels"] = data["commonLabels"]
    data["common_annotations"] = data["commonAnnotations"]

    del data["externalURL"]
    del data["groupKey"]
    del data["truncatedAlerts"]
    del data["groupLabels"]
    del data["commonLabels"]
    del data["commonAnnotations"]

    for alert in data["alerts"]:
        alert["starts_at"] = alert["startsAt"]
        alert["ends_at"] = alert["endsAt"]
        alert["generator_url"] = alert["generatorURL"]

        del alert["startsAt"]
        del alert["endsAt"]
        del alert["generatorURL"]


def add_specific(data: dict) -> None:
    """Add specific annotations and labels.

    Args:
        data (dict): Data dict to be modified in-place.
    """

    alerts = data["alerts"]

    for alert in alerts:
        annotations = alert["annotations"]
        alert["specific_annotations"] = {
            name: annotations[name]
            for name in set(annotations) - set(data["common_annotations"])
        }

        labels = alert["labels"]
        alert["specific_labels"] = {
            name: labels[name] for name in set(labels) - set(data["common_labels"])
        }
