"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

from prometheus_adaptive_cards.config import Route, Routing
from prometheus_adaptive_cards.model import (
    AlertGroup,
    EnhancedAlert,
    EnhancedAlertGroup,
)

from .actions import wrapped_add, wrapped_override, wrapped_remove
from .splitting import split
from .utils import add_specific


def preprocess(
    routing: Routing, route: Route, alert_group: AlertGroup
) -> list[EnhancedAlertGroup]:
    """Preprocess payload from Alertmanager.

    Args:
        routing (Routing): Routing related settings.
        route (Route): Route related settings.
        data (AlertGroup): Alertmanager payload.

    Returns:
        list[EnhancedAlertGroup]: List of one or more alert group. List will
            only contain more than one if the `split_by` feature is used.
    """

    wrapped_remove(routing.remove, route.remove, alert_group)
    wrapped_add(routing.add, route.add, alert_group)
    wrapped_override(routing.override, route.override, alert_group)

    alert_groups = (
        split(route.split_by.target, route.split_by.value, alert_group)
        if route.split_by
        else [alert_group]
    )

    enhanced_alert_groups = []

    for alert_group in alert_groups:
        add_specific(alert_group)

        enhanced_alerts = [
            EnhancedAlert.construct(**alert.dict()) for alert in alert_group.alerts
        ]
        del alert_group.alerts

        enhanced_alert_group = EnhancedAlertGroup.construct(**alert_group.dict())
        enhanced_alert_group.alerts = enhanced_alerts
        enhanced_alert_group.targets = [target.copy() for target in route.targets]
        enhanced_alert_groups.append(enhanced_alert_group)

    return enhanced_alert_groups
