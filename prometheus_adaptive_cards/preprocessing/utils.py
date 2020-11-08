"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

from prometheus_adaptive_cards.model import AlertGroup


def add_specific(alert_group: AlertGroup) -> None:
    alerts = alert_group.alerts

    for alert in alerts:
        alert.specific_annotations = {
            name: alert.annotations[name]
            for name in set(alert.annotations) - set(alert_group.common_annotations)
        }

        labels = alert.labels
        alert.specific_labels = {
            name: alert.labels[name]
            for name in set(alert.labels) - set(alert_group.common_labels)
        }
