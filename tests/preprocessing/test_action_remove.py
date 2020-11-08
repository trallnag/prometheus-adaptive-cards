"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import copy
import re

import pytest

import prometheus_adaptive_cards.preprocessing.actions as actions
from prometheus_adaptive_cards.config.settings import Remove, Route, Routing
from prometheus_adaptive_cards.model import Alert, AlertGroup

# ==============================================================================


@pytest.mark.actions_remove
def test_remove():
    target = "labels"
    keys = ["tim", "hans", "ute", "furz", "soda"]
    alert_group = AlertGroup.construct(
        **{
            f"common_{target}": {
                "tim": "schwenke",
                "hans": "meier",
            },
            "alerts": [
                Alert.construct(
                    **{
                        target: {
                            "tim": "schwenke",
                            "hans": "meier",
                            "ronald": "fritz",
                            "ute": "schneider",
                        }
                    }
                ),
                Alert.construct(
                    **{
                        target: {
                            "tim": "schwenke",
                            "hans": "meier",
                            "furz": "ernst",
                        }
                    }
                ),
            ],
        }
    )

    actions._remove(target, keys, alert_group)

    assert alert_group.__dict__[f"common_{target}"] == {}
    assert alert_group.alerts[0].__dict__[target] == {"ronald": "fritz"}
    assert alert_group.alerts[1].__dict__[target] == {}


# ==============================================================================


@pytest.mark.actions_remove_re
def test_remove_re():
    target = "labels"
    keys = [re.compile("^(tim|hans|ute|furz|soda)$")]
    alert_group = AlertGroup.construct(
        **{
            f"common_{target}": {
                "tim": "schwenke",
                "hans": "meier",
            },
            "alerts": [
                Alert.construct(
                    **{
                        target: {
                            "tim": "schwenke",
                            "hans": "meier",
                            "ronald": "fritz",
                            "ute": "schneider",
                        }
                    }
                ),
                Alert.construct(
                    **{
                        target: {
                            "tim": "schwenke",
                            "hans": "meier",
                            "furz": "ernst",
                        }
                    }
                ),
            ],
        }
    )

    actions._remove_re(target, keys, alert_group)

    assert alert_group.__dict__[f"common_{target}"] == {}
    assert alert_group.alerts[0].__dict__[target] == {"ronald": "fritz"}
    assert alert_group.alerts[1].__dict__[target] == {}


# ==============================================================================


@pytest.mark.actions_wrapped_remove
def test_wrapped_remove_none_none():
    alert_group = AlertGroup.construct(
        common_labels={
            "tim": "schwenke",
            "hans": "meier",
        },
        alerts=[
            Alert.construct(
                labels={
                    "tim": "schwenke",
                    "hans": "meier",
                    "ronald": "fritz",
                    "ute": "schneider",
                }
            ),
            Alert.construct(
                labels={
                    "tim": "schwenke",
                    "hans": "meier",
                    "furz": "ernst",
                }
            ),
        ],
    )

    a = None
    b = None

    actions.wrapped_remove(a, b, alert_group)

    assert alert_group.common_labels == {
        "tim": "schwenke",
        "hans": "meier",
    }

    assert alert_group.alerts[0].labels == {
        "tim": "schwenke",
        "hans": "meier",
        "ronald": "fritz",
        "ute": "schneider",
    }
    assert alert_group.alerts[1].labels == {
        "tim": "schwenke",
        "hans": "meier",
        "furz": "ernst",
    }


@pytest.mark.actions_wrapped_remove
def test_wrapped_remove_a_none():
    alert_group = AlertGroup.construct(
        common_labels={
            "tim": "schwenke",
            "hans": "meier",
        },
        alerts=[
            Alert.construct(
                labels={
                    "tim": "schwenke",
                    "hans": "meier",
                    "ronald": "fritz",
                    "ute": "schneider",
                }
            ),
            Alert.construct(
                labels={
                    "tim": "schwenke",
                    "hans": "meier",
                    "furz": "ernst",
                }
            ),
        ],
    )

    a = Remove(re_labels=[re.compile("^(tim|hans|ute|furz|soda)$")])
    b = None

    actions.wrapped_remove(a, b, alert_group)

    assert alert_group.common_labels == {}
    assert alert_group.alerts[0].labels == {"ronald": "fritz"}
    assert alert_group.alerts[1].labels == {}


@pytest.mark.actions_wrapped_remove
def test_wrapped_remove_none_b():
    alert_group = AlertGroup.construct(
        common_labels={
            "tim": "schwenke",
            "hans": "meier",
        },
        alerts=[
            Alert.construct(
                labels={
                    "tim": "schwenke",
                    "hans": "meier",
                    "ronald": "fritz",
                    "ute": "schneider",
                }
            ),
            Alert.construct(
                labels={
                    "tim": "schwenke",
                    "hans": "meier",
                    "furz": "ernst",
                }
            ),
        ],
    )

    a = None
    b = Remove(re_labels=[re.compile("^(tim|hans|ute|furz|soda)$")])

    actions.wrapped_remove(a, b, alert_group)

    assert alert_group.common_labels == {}
    assert alert_group.alerts[0].labels == {"ronald": "fritz"}
    assert alert_group.alerts[1].labels == {}


@pytest.mark.actions_wrapped_remove
def test_wrapped_remove_a_b():
    alert_group = AlertGroup.construct(
        common_annotations={},
        common_labels={
            "tim": "schwenke",
            "hans": "meier",
        },
        alerts=[
            Alert.construct(
                annotations={},
                labels={
                    "tim": "schwenke",
                    "hans": "meier",
                    "ronald": "fritz",
                    "ute": "schneider",
                },
            ),
            Alert.construct(
                annotations={},
                labels={
                    "tim": "schwenke",
                    "hans": "meier",
                    "furz": "ernst",
                },
            ),
        ],
    )

    a = Remove(
        labels=["ute", "tim", "furz"],
        annotations=["ute", "tim", "furz"],
    )
    b = Remove(
        re_annotations=[re.compile("^(tim|hans)$")],
        re_labels=[re.compile("^(tim|hans)$")],
    )

    actions.wrapped_remove(a, b, alert_group)

    assert alert_group.common_annotations == {}
    assert alert_group.common_labels == {}
    assert alert_group.alerts[0].annotations == {}
    assert alert_group.alerts[0].labels == {"ronald": "fritz"}
    assert alert_group.alerts[1].annotations == {}
    assert alert_group.alerts[1].labels == {}


# ==============================================================================
