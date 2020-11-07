"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""


import copy

import prometheus_adaptive_cards.preprocessing.utils as utils

# ==============================================================================


def test_convert_to_snake_case():
    data = {
        "receiver": "generic",
        "status": "firing",
        "alerts": [
            {
                "status": "firing",
                "labels": {
                    "alertname": "WhatEver",
                    "foo_bar_qux": "foo_moo_zoom",
                    "severity": "warning",
                },
                "annotations": {
                    "description": "A Prometheus job has disa",
                    "summary": "Prometheus job missing (instance )",
                },
                "startsAt": "2020-11-03T17:51:36.14925565Z",
                "endsAt": "0001-01-01T00:00:00Z",
                "generatorURL": "http://9e6d80bea9ef:9090/graph?g0.e",
                "fingerprint": "d57ff78af6ac95e8",
            }
        ],
        "groupLabels": {"alertname": "WhatEver"},
        "commonLabels": {
            "alertname": "WhatEver",
            "foo_bar_qux": "foo_moo_zoom",
            "severity": "warning",
        },
        "commonAnnotations": {
            "description": "A Prometheus job has disappep[]",
            "summary": "Prometheus job missing (instance )",
        },
        "externalURL": "http://1217896f2a1d:9093",
        "version": "4",
        "groupKey": '{}:{alertname="WhatEver"}',
        "truncatedAlerts": 0,
    }

    utils.convert_to_snake_case(data)

    assert data == {
        "receiver": "generic",
        "status": "firing",
        "alerts": [
            {
                "status": "firing",
                "labels": {
                    "alertname": "WhatEver",
                    "foo_bar_qux": "foo_moo_zoom",
                    "severity": "warning",
                },
                "annotations": {
                    "description": "A Prometheus job has disa",
                    "summary": "Prometheus job missing (instance )",
                },
                "starts_at": "2020-11-03T17:51:36.14925565Z",
                "ends_at": "0001-01-01T00:00:00Z",
                "generator_url": "http://9e6d80bea9ef:9090/graph?g0.e",
                "fingerprint": "d57ff78af6ac95e8",
            }
        ],
        "group_labels": {"alertname": "WhatEver"},
        "common_labels": {
            "alertname": "WhatEver",
            "foo_bar_qux": "foo_moo_zoom",
            "severity": "warning",
        },
        "common_annotations": {
            "description": "A Prometheus job has disappep[]",
            "summary": "Prometheus job missing (instance )",
        },
        "external_url": "http://1217896f2a1d:9093",
        "version": "4",
        "group_key": '{}:{alertname="WhatEver"}',
        "truncated_alerts": 0,
    }


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
    data = copy.deepcopy(DATA)

    data["alerts"][0]["annotations"].update(
        {"specific": "specific", "very_specific": "very_specific"}
    )

    utils.add_specific(data)

    assert data["alerts"][0]["specific_annotations"]["specific"] == "specific"

    assert data["alerts"][0]["specific_annotations"] is not None
    assert data["alerts"][1]["specific_annotations"] is not None

    assert data["alerts"][0]["specific_labels"] is not None
    assert data["alerts"][1]["specific_labels"] is not None


def test_add_specific_labels():
    data = copy.deepcopy(DATA)

    data["alerts"][0]["labels"].update(
        {"specific": "specific", "very_specific": "very_specific"}
    )

    utils.add_specific(data)

    assert data["alerts"][0]["specific_labels"]["specific"] == "specific"

    assert data["alerts"][0]["specific_labels"] is not None
    assert data["alerts"][1]["specific_labels"] is not None


# ==============================================================================
