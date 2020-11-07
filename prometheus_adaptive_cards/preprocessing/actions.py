"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

from typing import Literal, Optional, Pattern

from loguru import logger

from prometheus_adaptive_cards.config import Add, Override, Remove, Route, Routing

# ==============================================================================
# Remove action


def _remove(
    target: Literal["annotations", "labels"], keys: list[str], data: dict
) -> None:
    """Removes in-place.

    Given `data` must have the following structure:

    ```python
    {
        "common_${target}": {"key": "value"},
        "alerts": [
            {
                "${target}": {"key": "value"}
            }
        ]
    }
    ```

    Args:
        target (Literal["annotations", "labels"]): What to target.
        names (list[str]): Keys to remove.
        data (dict): Data dict to mutate in-place.
    """

    keys = set(keys)

    for key in keys:
        value = data[f"common_{target}"].pop(key, None)
        for alert in data["alerts"]:
            value = alert[target].pop(key, None)


def _remove_re(target: str, re_patterns: list[Pattern], data: dict) -> None:
    """Removes in-place.

    Given `data` must have the following structure:

    ```python
    {
        "common_${target}": {"key": "value"},
        "alerts": [
            {
                "${target}": {"key": "value"}
            }
        ]
    }
    ```

    Args:
        target (str): Must be either `annotations` or `labels`.
        re_patterns (list[Pattern]): List of patterns.
        data (dict): Data dict to mutate in-place.
    """

    for pattern in re_patterns:
        elements = data[f"common_{target}"]
        elements_to_pop = {e for e in elements if pattern.search(e)}
        popped_values = [elements.pop(e) for e in elements_to_pop]

        for alert in data["alerts"]:
            elements = alert[target]
            elements_to_pop = {e for e in elements if pattern.search(e)}
            popped_values = [elements.pop(e) for e in elements_to_pop]


def wrapped_remove(r1: Optional[Remove], r2: Optional[Remove], data: dict) -> None:
    """Uses two Remove objects to mutate data.

    Given `data` must have the following structure:

    ```python
    {
        "common_annotations": {"key": "value"},
        "common_labels": {"key": "value"},
        "alerts": [
            {
                "annotations": {"key": "value"},
                "labels": {"key": "value"},
            }
        ]
    }
    ```

    Args:
        r1 (Optional[Remove]): Remove object 1.
        r2 (Optional[Remove]): Remove object 2.
        data (dict): Data to mutate in-place.
    """

    if r1 and r2:
        annotations = r1.annotations + r2.annotations
        labels = r1.labels + r2.labels
        re_annotations = r1.re_annotations + r2.re_annotations
        re_labels = r1.re_labels + r2.re_labels
    elif r1:
        annotations = r1.annotations
        labels = r1.labels
        re_annotations = r1.re_annotations
        re_labels = r1.re_labels
    elif r2:
        annotations = r2.annotations
        labels = r2.labels
        re_annotations = r2.re_annotations
        re_labels = r2.re_labels
    else:
        return

    if annotations:
        _remove("annotations", annotations, data)
    if labels:
        _remove("labels", labels, data)
    if re_annotations:
        _remove_re("annotations", re_annotations, data)
    if re_labels:
        _remove_re("labels", re_labels, data)


# ==============================================================================
# Add action


def _add(
    target: Literal["annotations", "labels"], items: dict[str, str], data: dict
) -> None:
    """Adds items in-place.

    Given `data` must have the following structure:

    ```python
    {
        "common_${target}": {"key": "value"},
        "alerts": [
            {
                "${target}": {"key": "value"}
            }
        ]
    }
    ```

    Args:
        target (Literal["annotations", "labels"]): What to target.
        items (dict[str, str]): Items to add.
        data (dict): Data dict to mutate in-place.
    """

    for name, value in items.items():
        unique_values = set()
        for alert in data["alerts"]:
            elements = alert[target]
            if name not in elements:
                elements[name] = value
                unique_values.add(value)
            else:
                unique_values.add(elements[name])
        if len(unique_values) == 1 and value in unique_values:
            data[f"common_{target}"][name] = value


def wrapped_add(a1: Optional[Add], a2: Optional[Add], data: dict) -> None:
    """Uses two Add objects to mutate data.

    Given `data` must have the following structure:

    ```python
    {
        "common_annotations": {"key": "value"},
        "common_labels": {"key": "value"},
        "alerts": [
            {
                "annotations": {"key": "value"},
                "labels": {"key": "value"},
            }
        ]
    }
    ```

    Args:
        a1 (Optional[Add]): Add object 1.
        a2 (Optional[Add]): Add object 2.
        data (dict): Data to mutate in-place.
    """

    if a1 and a2:
        annotations = a1.annotations | a2.annotations
        labels = a1.labels | a2.labels
    elif a1:
        annotations = a1.annotations
        labels = a1.labels
    elif a2:
        annotations = a2.annotations
        labels = a2.labels
    else:
        return

    if annotations:
        _add("annotations", annotations, data)
    if labels:
        _add("labels", labels, data)


# ==============================================================================


def _override(
    target: Literal["annotations", "labels"], items: dict[str, str], data: dict
) -> None:
    """Add and overrides item in-place.

    ```python
    {
        "common_${target}": {"key": "value"},
        "alerts": [
            {
                "${target}": {"key": "value"}
            }
        ]
    }
    ```

    Args:
        target (Literal["annotations", "labels"]): What to target.
        items (dict[str, str]): Items to override with.
        data (dict): Data dict to mutate in-place.
    """

    for name, value in items.items():
        data[f"common_{target}"][name] = value
        for alert in data["alerts"]:
            elements = alert[target]
            elements[name] = value


def wrapped_override(o1: Optional[Override], o2: Optional[Override], data: dict) -> None:
    """Uses two Override objects to mutate data.

    Given `data` must have the following structure:

    ```python
    {
        "common_annotations": {"key": "value"},
        "common_labels": {"key": "value"},
        "alerts": [
            {
                "annotations": {"key": "value"},
                "labels": {"key": "value"},
            }
        ]
    }
    ```

    Args:
        o1 (Optional[Override]): Override object 1.
        o2 (Optional[Override]): Override object 2.
        data (dict): Data to mutate in-place.
    """

    if o1 and o2:
        annotations = o1.annotations | o2.annotations
        labels = o1.labels | o2.labels
    elif o1:
        annotations = o1.annotations
        labels = o1.labels
    elif o2:
        annotations = o2.annotations
        labels = o2.labels
    else:
        return

    if annotations:
        _override("annotations", annotations, data)
    if labels:
        _override("labels", labels, data)


# ==============================================================================
