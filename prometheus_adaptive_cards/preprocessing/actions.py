"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

from typing import Pattern

from loguru import logger

from prometheus_adaptive_cards.api.models import Data
from prometheus_adaptive_cards.config.settings import Route, Routing


def _remove(target: str, names: list[str], data: Data) -> None:
    """Removes annotations / labels in-place.

    Args:
        target (str): Must be either `annotations` or `labels`.
        names (list[str]): Keys to remove.
        data (Data): Data to mutate in-place.
    """

    names = set(names)

    for name in names:
        value = data.__dict__[f"common_{target}"].pop(name, None)
        if value:
            logger.bind(name=name, value=value).debug(f"Removed common {target}.")
        for alert in data.alerts:
            value = alert.__dict__[target].pop(name, None)
            if value:
                logger.bind(alert=alert.fingerprint, name=name, value=value).debug(
                    f"Removed {target}."
                )


def _remove_re(target: str, re_patterns: list[Pattern], data: Data) -> None:
    """Removes in-place from data that match unanchored pattern.

    Args:
        target (str): Must be either `annotations` or `labels`.
        re_patterns (list[Pattern]): List of patterns.
        data (Data): Data to mutate in-place.
    """

    for pattern in re_patterns:
        elements = data.__dict__[f"common_{target}"]
        elements_to_pop = {e for e in elements if pattern.search(e)}
        popped_values = [elements.pop(e) for e in elements_to_pop]

        if popped_values:
            logger.bind(
                removed=dict(zip(elements_to_pop, popped_values)),
                pattern=pattern.pattern,
            ).info(f"Removed {target} which name matched unachored pattern.")

        for alert in data.alerts:
            elements = alert.__dict__[target]
            elements_to_pop = {e for e in elements if pattern.search(e)}
            popped_values = [elements.pop(e) for e in elements_to_pop]

            if popped_values:
                logger.bind(
                    removed=dict(zip(elements_to_pop, popped_values)),
                    pattern=pattern.pattern,
                    alert=alert.fingerprint,
                ).info(f"Removed {target} which name matched unachored pattern.")


def _add(target: str, items: dict[str, str], data: Data) -> None:
    """Adds items to annotations / labels in-place.

    Args:
        target (str): Must be either `annotations` or `labels`.
        items (dict[str, str]): Items to add.
        data (Data): Data to mutate in-place.
    """

    for name, value in items.items():
        unique_values = set()
        for alert in data.alerts:
            elements = alert.__dict__[target]
            if name not in elements:
                elements[name] = value
                unique_values.add(value)
                logger.bind(
                    alert=alert.fingerprint,
                    name=name,
                    value=value,
                ).info(f"Added to alert {target}.")
            else:
                unique_values.add(elements[name])
        if len(unique_values) == 1:
            data.__dict__[f"common_{target}"].__setitem__(name, value)
            logger.bind(
                name=name,
                value=value,
            ).info(f"Added to common {target}.")


def _override(target: str, items: dict[str, str], data: Data) -> None:
    """Override annotations / labels in-place.

    Args:
        target (str): Must be either `annotations` or `labels`.
        items (dict[str, str]): Items to override with.
        data (Data): Data to mutate in-place.
    """

    for name, value in items.items():
        data.__dict__[f"common_{target}"].__setitem__(name, value)
        for alert in data.alerts:
            elements = alert.__dict__[target]
            elements[name] = value
        logger.bind(name=name, value=value).info(f"Overridden item {target}.")


# ==============================================================================


def perform_actions(routing: Routing, route: Route, data: Data) -> None:
    """Perform actions defined in routing and route settings in-place on data."""

    logger.info("Start performing remove, add and override actions.")

    # --------------------------------------------------------------------------

    annotations = route.remove.annotations + routing.remove.annotations
    if len(annotations) > 0:
        _remove("annotations", annotations, data)

    labels = route.remove.labels + routing.remove.labels
    if len(labels) > 0:
        _remove("labels", labels, data)

    # --------------------------------------------------------------------------

    annotations = route.remove.re_annotations + routing.remove.re_annotations
    if len(annotations) > 0:
        _remove_re("annotations", annotations, data)

    labels = route.remove.re_labels + routing.remove.re_labels
    if len(annotations) > 0:
        _remove_re("labels", labels, data)

    # --------------------------------------------------------------------------

    annotations = route.add.annotations | routing.add.annotations
    if len(annotations) > 0:
        _add("annotations", annotations, data)

    labels = route.add.labels | routing.add.labels
    if len(labels) > 0:
        _add("labels", labels, data)

    # --------------------------------------------------------------------------

    annotations = route.override.annotations | routing.override.annotations
    if len(annotations) > 0:
        _override("annotations", annotations, data)

    labels = route.add.labels | routing.add.labels
    if len(labels) > 0:
        _override("labels", labels, data)

    # --------------------------------------------------------------------------

    logger.info("Finished performing remove, add and override actions.")


# ==============================================================================
