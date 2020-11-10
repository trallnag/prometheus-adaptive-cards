"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

from prometheus_adaptive_cards.config.settings import (
    Add,
    Override,
    Remove,
    Route,
    Routing,
)
from prometheus_adaptive_cards.model import Alert, AlertGroup
from prometheus_adaptive_cards.preprocessing.preprocessing import preprocess


def test_preprocess(helpers):
    routing = Routing(
        remove=Remove(
            annotations=["vw", "audi"],
            labels=["heinz"],
            re_annotations=["^(mercedes)$", "^__.*$"],
            re_labels=["^__.*$"],
        ),
        add=Add(
            annotations={"bmw": "value"},
            labels={"simon": "humben"},
        ),
        override=Override(
            annotations={"yung": "hurn"},
            labels={"old": "barn"},
        ),
    )

    route = Route(
        name="whatever",
        add=Add(
            annotations={"bmw": "value"},
            labels={"simon": "klumpen"},
        ),
    )

    alert_group = AlertGroup.construct(
        group_labels={"alertname": "WhatEver"},
        common_labels={"heinz": "meier", "__meta": "x", "severity": "warning"},
        common_annotations={
            "vw": "x",
        },
        alerts=[
            Alert.construct(
                labels={
                    "heinz": "meier",
                    "__meta": "x",
                    "severity": "warning",
                    "yung": "barn",
                },
                annotations={
                    "vw": "x",
                    "audi": "x",
                    "yung": "barn",
                },
            ),
            Alert.construct(
                labels={
                    "heinz": "meier",
                    "simon": "fart",
                    "__meta": "x",
                    "severity": "warning",
                },
                annotations={
                    "vw": "x",
                },
            ),
        ],
    )

    alertgroup = preprocess(routing, route, alert_group)[0]

    helpers.print_struct(alertgroup)

    assert alertgroup.common_labels == {
        "severity": "warning",
        "old": "barn",
    }

    assert alertgroup.common_annotations == {
        "bmw": "value",
        "yung": "hurn",
    }

    assert alertgroup.alerts[0].labels == {
        "severity": "warning",
        "yung": "barn",
        "old": "barn",
        "simon": "klumpen",
    }

    assert alertgroup.alerts[0].annotations == {
        "yung": "hurn",
        "bmw": "value",
    }

    assert alertgroup.alerts[1].labels == {
        "simon": "fart",
        "severity": "warning",
        "simon": "fart",
        "old": "barn",
    }

    assert alertgroup.alerts[1].annotations == {
        "bmw": "value",
        "yung": "hurn",
    }
