"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import prometheus_adaptive_cards.preprocessing.actions as actions
from prometheus_adaptive_cards.config.settings import Override
from prometheus_adaptive_cards.model import Alert, AlertGroup

# ==============================================================================


def test_override():
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

    actions._override(
        "labels",
        {
            "tim": "schwonkel",
            "ute": "freier",
            "frank": "sohn",
        },
        alert_group,
    )

    assert alert_group.common_labels == {
        "tim": "schwonkel",
        "ute": "freier",
        "frank": "sohn",
    }
    assert alert_group.alerts[0].labels == {
        "tim": "schwonkel",
        "ute": "freier",
        "frank": "sohn",
    }
    assert alert_group.alerts[1].labels == {
        "tim": "schwonkel",
        "ute": "freier",
        "frank": "sohn",
    }


# ==============================================================================


def test_wrapped_override_none_none():
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

    actions.wrapped_override(a, b, alert_group)

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


def test_wrapped_override_a_none():
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

    a = Override(
        labels={
            "tim": "schwonkel",
            "ute": "freier",
            "frank": "sohn",
        }
    )
    b = None

    actions.wrapped_override(a, b, alert_group)

    assert alert_group.common_labels == {
        "tim": "schwonkel",
        "ute": "freier",
        "frank": "sohn",
    }
    assert alert_group.alerts[0].labels == {
        "tim": "schwonkel",
        "ute": "freier",
        "frank": "sohn",
    }
    assert alert_group.alerts[1].labels == {
        "tim": "schwonkel",
        "ute": "freier",
        "frank": "sohn",
    }


def test_wrapped_override_none_b():
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

    b = Override(
        labels={
            "tim": "schwonkel",
            "ute": "freier",
            "frank": "sohn",
        }
    )
    a = None

    actions.wrapped_override(a, b, alert_group)

    assert alert_group.common_labels == {
        "tim": "schwonkel",
        "ute": "freier",
        "frank": "sohn",
    }
    assert alert_group.alerts[0].labels == {
        "tim": "schwonkel",
        "ute": "freier",
        "frank": "sohn",
    }
    assert alert_group.alerts[1].labels == {
        "tim": "schwonkel",
        "ute": "freier",
        "frank": "sohn",
    }


def test_wrapped_override_a_b():
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

    a = Override(
        labels={
            "tim": "schwonkel",
            "ute": "freier",
        }
    )
    b = Override(
        labels={
            "ute": "freier",
            "frank": "sohn",
        }
    )

    actions.wrapped_override(a, b, alert_group)

    assert alert_group.common_labels == {
        "tim": "schwonkel",
        "ute": "freier",
        "frank": "sohn",
    }
    assert alert_group.alerts[0].labels == {
        "tim": "schwonkel",
        "ute": "freier",
        "frank": "sohn",
    }
    assert alert_group.alerts[1].labels == {
        "tim": "schwonkel",
        "ute": "freier",
        "frank": "sohn",
    }


# ==============================================================================
