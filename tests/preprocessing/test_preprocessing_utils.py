"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import prometheus_adaptive_cards.preprocessing.utils as utils
from prometheus_adaptive_cards.model import Alert, AlertGroup

# ==============================================================================


DATA = {
    "common_labels": {
        "alertname": "JustATestAlert",
        "namespace": "whatever/promstack",
        "severity": "info",
    },
    "common_annotations": {
        "investigate_link": "https://domain.com/grafanMz/container-intra",
        "summary": "Ratio(Max(Working Set, RSS) / Reservation) [5m Avg] \\u003c 40 %",
        "title": "Memory: Relativ memory usage low",
    },
    "alerts": [
        {
            "labels": {
                "alertname": "JustATestAlert",
                "name": "grafana",
                "namespace": "whatever/promstack",
                "severity": "info",
            },
            "annotations": {
                "description": "Lorem ipsum dolor sit",
                "investigate_link": "https://domain.com/grafanainer-intra",
                "summary": "Ratio(Max(Working Set, RSS) / Reserg] \\u003c 40 %",
                "title": "Memory: Relativ memory usage low",
            },
        },
        {
            "labels": {
                "alertname": "JustATestAlert",
                "name": "grafana",
                "namespace": "whatever/promstack",
                "severity": "info",
            },
            "annotations": {
                "description": "Lorem ipsum dolor sit amete value 2.",
                "investigate_link": "https://domain.com/graontainer-intra",
                "summary": "Ratio(Max(Workition) [5m Avg] \\u003c 40 %",
                "title": "Memory: Relativ memory usage low",
            },
        },
    ],
}


def test_add_specific_annotations():
    alert_group = AlertGroup.construct(
        common_labels={
            "alertname": "JustATestAlert",
            "namespace": "whatever/promstack",
            "severity": "info",
        },
        common_annotations={
            "investigate_link": "https://domain.com/grafanMz/container-intra",
            "summary": "Ratio(Max(Working Set, RSS) / Reservation) [5m Avg] \\u003c 40 %",
            "title": "Memory: Relativ memory usage low",
        },
        alerts=[
            Alert.construct(
                labels={
                    "alertname": "JustATestAlert",
                    "name": "grafana",
                    "namespace": "whatever/promstack",
                    "severity": "info",
                },
                annotations={
                    "description": "Lorem ipsum dolor sit",
                    "investigate_link": "https://domain.com/grafanainer-intra",
                    "summary": "Ratio(Max(Working Set, RSS) / Reserg] \\u003c 40 %",
                    "title": "Memory: Relativ memory usage low",
                    "specific": "specific",
                    "very_specific": "very_specific",
                },
            ),
            Alert.construct(
                labels={
                    "alertname": "JustATestAlert",
                    "name": "grafana",
                    "namespace": "whatever/promstack",
                    "severity": "info",
                },
                annotations={
                    "description": "Lorem ipsum dolor sit amete value 2.",
                    "investigate_link": "https://domain.com/graontainer-intra",
                    "summary": "Ratio(Max(Workition) [5m Avg] \\u003c 40 %",
                    "title": "Memory: Relativ memory usage low",
                },
            ),
        ],
    )

    utils.add_specific(alert_group)

    assert alert_group.alerts[0].specific_annotations["specific"] == "specific"
    assert alert_group.alerts[0].specific_annotations["very_specific"] == "very_specific"

    assert alert_group.alerts[0].specific_annotations is not None
    assert alert_group.alerts[1].specific_annotations is not None

    assert alert_group.alerts[0].specific_labels is not None
    assert alert_group.alerts[1].specific_labels is not None


def test_add_specific_labels():
    alert_group = AlertGroup.construct(
        common_labels={
            "alertname": "JustATestAlert",
            "namespace": "whatever/promstack",
            "severity": "info",
        },
        common_annotations={
            "investigate_link": "https://domain.com/grafanMz/container-intra",
            "summary": "Ratio(Max(Working Set, RSS) / Reservation) [5m Avg] \\u003c 40 %",
            "title": "Memory: Relativ memory usage low",
        },
        alerts=[
            Alert.construct(
                labels={
                    "alertname": "JustATestAlert",
                    "name": "grafana",
                    "namespace": "whatever/promstack",
                    "severity": "info",
                    "specific": "specific",
                    "very_specific": "very_specific",
                },
                annotations={
                    "description": "Lorem ipsum dolor sit",
                    "investigate_link": "https://domain.com/grafanainer-intra",
                    "summary": "Ratio(Max(Working Set, RSS) / Reserg] \\u003c 40 %",
                    "title": "Memory: Relativ memory usage low",
                    "specific": "specific",
                    "very_specific": "very_specific",
                },
            ),
            Alert.construct(
                labels={
                    "alertname": "JustATestAlert",
                    "name": "grafana",
                    "namespace": "whatever/promstack",
                    "severity": "info",
                },
                annotations={
                    "description": "Lorem ipsum dolor sit amete value 2.",
                    "investigate_link": "https://domain.com/graontainer-intra",
                    "summary": "Ratio(Max(Workition) [5m Avg] \\u003c 40 %",
                    "title": "Memory: Relativ memory usage low",
                },
            ),
        ],
    )

    utils.add_specific(alert_group)

    assert alert_group.alerts[0].specific_labels["specific"] == "specific"

    assert alert_group.alerts[0].specific_labels is not None
    assert alert_group.alerts[1].specific_labels is not None


# ==============================================================================
