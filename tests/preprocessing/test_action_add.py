"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import prometheus_adaptive_cards.preprocessing.actions as actions
from prometheus_adaptive_cards.config.settings import Add
from prometheus_adaptive_cards.model import Alert, AlertGroup

# ==============================================================================


def test_add():
    alert_group = AlertGroup.construct(
        common_labels={
            "tim": "schwenke",
        },
        alerts=[
            Alert.construct(
                labels={
                    "tim": "schwenke",
                    "ute": "meier",
                    "frank": "sohn",
                }
            ),
            Alert.construct(
                labels={
                    "tim": "schwenke",
                }
            ),
        ],
    )

    actions._add(
        "labels",
        {
            "tim": "schwonkel",
            "ute": "freier",
            "frank": "sohn",
        },
        alert_group,
    )

    assert alert_group.common_labels == {
        "tim": "schwenke",
        "frank": "sohn",
    }
    assert alert_group.alerts[0].labels == {
        "tim": "schwenke",
        "ute": "meier",
        "frank": "sohn",
    }
    assert alert_group.alerts[1].labels == {
        "tim": "schwenke",
        "ute": "freier",
        "frank": "sohn",
    }


# ==============================================================================


def test_wrapped_add_none_none():
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

    actions.wrapped_add(None, None, alert_group)

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


def test_wrapped_add_a1_none():
    alert_group = AlertGroup.construct(
        common_labels={
            "tim": "schwenke",
        },
        alerts=[
            Alert.construct(
                labels={
                    "tim": "schwenke",
                    "ute": "meier",
                    "frank": "sohn",
                }
            ),
            Alert.construct(
                labels={
                    "tim": "schwenke",
                }
            ),
        ],
    )

    a1 = Add(
        labels={
            "tim": "schwonkel",
            "ute": "freier",
            "frank": "sohn",
        }
    )
    a2 = None

    actions.wrapped_add(a1, a2, alert_group)

    assert alert_group.common_labels == {
        "tim": "schwenke",
        "frank": "sohn",
    }
    assert alert_group.alerts[0].labels == {
        "tim": "schwenke",
        "ute": "meier",
        "frank": "sohn",
    }
    assert alert_group.alerts[1].labels == {
        "tim": "schwenke",
        "ute": "freier",
        "frank": "sohn",
    }


def test_wrapped_add_none_a2():
    alert_group = AlertGroup.construct(
        common_labels={
            "tim": "schwenke",
        },
        alerts=[
            Alert.construct(
                labels={
                    "tim": "schwenke",
                    "ute": "meier",
                    "frank": "sohn",
                }
            ),
            Alert.construct(
                labels={
                    "tim": "schwenke",
                }
            ),
        ],
    )

    a2 = Add(
        labels={
            "tim": "schwonkel",
            "ute": "freier",
            "frank": "sohn",
        }
    )
    a1 = None

    actions.wrapped_add(a1, a2, alert_group)

    assert alert_group.common_labels == {
        "tim": "schwenke",
        "frank": "sohn",
    }
    assert alert_group.alerts[0].labels == {
        "tim": "schwenke",
        "ute": "meier",
        "frank": "sohn",
    }
    assert alert_group.alerts[1].labels == {
        "tim": "schwenke",
        "ute": "freier",
        "frank": "sohn",
    }


def test_wrapped_add_a1_a2():
    alert_group = AlertGroup.construct(
        common_labels={
            "tim": "schwenke",
        },
        alerts=[
            Alert.construct(
                labels={
                    "tim": "schwenke",
                    "ute": "meier",
                    "frank": "sohn",
                }
            ),
            Alert.construct(
                labels={
                    "tim": "schwenke",
                }
            ),
        ],
    )

    a1 = Add(
        labels={
            "tim": "schwonkel",
            "ute": "freier",
        }
    )
    a2 = Add(
        labels={
            "ute": "freier",
            "frank": "sohn",
        }
    )

    actions.wrapped_add(a1, a2, alert_group)

    assert alert_group.common_labels == {
        "tim": "schwenke",
        "frank": "sohn",
    }
    assert alert_group.alerts[0].labels == {
        "tim": "schwenke",
        "ute": "meier",
        "frank": "sohn",
    }
    assert alert_group.alerts[1].labels == {
        "tim": "schwenke",
        "ute": "freier",
        "frank": "sohn",
    }


# ==============================================================================
