"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

from fastapi import Request

from prometheus_adaptive_cards.config import Route, Routing
from prometheus_adaptive_cards.model import Alert, AlertGroup

from .actions import wrapped_add, wrapped_override, wrapped_remove
from .splitting import split
from .utils import add_specific, convert_to_snake_case


def preprocess(
    request: Request, routing: Routing, route: Route, data: dict
) -> list[AlertGroup]:
    """Preprocess payload data and turn it a set of objects ready for templating.

    Args:
        request (Request): The request the data is part of.
        routing (Routing): Routing related settings.
        route (Route): Route related settings.
        data (dict): Alertmanager payload.

    Returns:
        list[AlertGroup]: List of enhanced data objects. If splitting is not
            used this list will always contain a single element.
    """

    convert_to_snake_case(data)

    data["request"] = request

    wrapped_remove(routing.remove, route.remove, data)
    wrapped_add(routing.add, route.add, data)
    wrapped_override(routing.override, route.override, data)

    datas = (
        split(route.split_by.target, route.split_by.value, data)
        if route.split_by
        else [data]
    )

    alert_groups = []

    for data in datas:
        add_specific(data)
        data["alerts"] = [Alert(**alert) for alert in data["alerts"]]
        alert_groups.append(AlertGroup(**data))

    return alert_groups
