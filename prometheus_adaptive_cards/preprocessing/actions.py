"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

from typing import Literal, Optional, Pattern

from prometheus_adaptive_cards.config import Add, Override, Remove
from prometheus_adaptive_cards.model import AlertGroup

# ==============================================================================
# Remove action


def _remove(
    target: Literal["annotations", "labels"], keys: list[str], alert_group: AlertGroup
) -> None:
    """Removes annotations / labels in-place from alert group.

    Args:
        target (Literal["annotations", "labels"]): What to target.
        keys (list[str]): Keys to remove.
        alert_group (AlertGroup): Alert group to work with.
    """

    for key in set(keys):
        alert_group.__dict__[f"common_{target}"].pop(key, None)
        for alert in alert_group.alerts:
            alert.__dict__[target].pop(key, None)


def _remove_re(target: str, re_keys: list[Pattern], alert_group: AlertGroup) -> None:
    """Removes annotations / labels in-place from alert group.

    Args:
        target (Literal["annotations", "labels"]): What to target.
        re_keys (list[Pattern]): List of patterns.
        alert_group (AlertGroup): Alert group to work with.
    """

    for pattern in re_keys:
        elements = alert_group.__dict__[f"common_{target}"]
        for element_to_pop in {e for e in elements if pattern.search(e)}:
            elements.pop(element_to_pop)

        for alert in alert_group.alerts:
            elements = alert.__dict__[target]
            for element_to_pop in {e for e in elements if pattern.search(e)}:
                elements.pop(element_to_pop)


def wrapped_remove(
    a: Optional[Remove], b: Optional[Remove], alert_group: AlertGroup
) -> None:
    """Applies to Remove objects on alert group in-place.

    Args:
        a (Optional[Remove]): Remove object 1.
        b (Optional[Remove]): Remove object 2.
        alert_group (AlertGroup): Data to mutate in-place.
    """

    if a and b:
        annotations = a.annotations + b.annotations
        labels = a.labels + b.labels
        re_annotations = a.re_annotations + b.re_annotations
        re_labels = a.re_labels + b.re_labels
    elif a:
        annotations = a.annotations
        labels = a.labels
        re_annotations = a.re_annotations
        re_labels = a.re_labels
    elif b:
        annotations = b.annotations
        labels = b.labels
        re_annotations = b.re_annotations
        re_labels = b.re_labels
    else:
        return

    if annotations:
        _remove("annotations", annotations, alert_group)
    if labels:
        _remove("labels", labels, alert_group)
    if re_annotations:
        _remove_re("annotations", re_annotations, alert_group)
    if re_labels:
        _remove_re("labels", re_labels, alert_group)


# ==============================================================================
# Add action


def _add(
    target: Literal["annotations", "labels"],
    items: dict[str, str],
    alert_group: AlertGroup,
) -> None:
    """Adds annotations / labels in-place from alert group without updating.

    Args:
        target (Literal["annotations", "labels"]): What to target.
        items (dict[str, str]): Items to add.
        alert_group (AlertGroup): Alert group to work with.
    """

    for name, value in items.items():
        unique_values = set()
        for alert in alert_group.alerts:
            elements = alert.__dict__[target]
            if name not in elements:
                elements[name] = value
                unique_values.add(value)
            else:
                unique_values.add(elements[name])
        if len(unique_values) == 1 and value in unique_values:
            alert_group.__dict__[f"common_{target}"][name] = value


def wrapped_add(a: Optional[Add], b: Optional[Add], alert_group: AlertGroup) -> None:
    """Applies to Add objects on alert group in-place.

    Args:
        a (Optional[Add]): Add object 1.
        b (Optional[Add]): Add object 2.
        alert_group (AlertGroup): Data to mutate in-place.
    """

    if a and b:
        annotations = a.annotations | b.annotations
        labels = a.labels | b.labels
    elif a:
        annotations = a.annotations
        labels = a.labels
    elif b:
        annotations = b.annotations
        labels = b.labels
    else:
        return

    if annotations:
        _add("annotations", annotations, alert_group)
    if labels:
        _add("labels", labels, alert_group)


# ==============================================================================


def _override(
    target: Literal["annotations", "labels"],
    items: dict[str, str],
    alert_group: AlertGroup,
) -> None:
    """Adds and overrides annotations / labels in-place from alert group.

    Args:
        target (Literal["annotations", "labels"]): What to target.
        items (dict[str, str]): Items to override and add.
        alert_group (AlertGroup): Alert group to work with.
    """

    for name, value in items.items():
        alert_group.__dict__[f"common_{target}"][name] = value
        for alert in alert_group.alerts:
            alert.__dict__[target][name] = value


def wrapped_override(
    a: Optional[Override], b: Optional[Override], alert_group: AlertGroup
) -> None:
    """Applies two Override objects on alert group in-place.

    Args:
        a (Optional[Override]): Override object 1.
        b (Optional[Override]): Override object 2.
        alert_group (AlertGroup): Data to mutate in-place.
    """

    if a and b:
        annotations = a.annotations | b.annotations
        labels = a.labels | b.labels
    elif a:
        annotations = a.annotations
        labels = a.labels
    elif b:
        annotations = b.annotations
        labels = b.labels
    else:
        return

    if annotations:
        _override("annotations", annotations, alert_group)
    if labels:
        _override("labels", labels, alert_group)


# ==============================================================================
