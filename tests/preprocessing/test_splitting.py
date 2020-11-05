"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import prometheus_adaptive_cards.preprocessing.splitting as splitting

# ==============================================================================


def test_group_alerts_single_alert(caplog):
    list_of_alert_lists = splitting._group_alerts(
        "annotations", "foo", [{"annotations": {"foo": "bar"}}]
    )
    assert list_of_alert_lists == [[{"annotations": {"foo": "bar"}}]]

    list_of_alert_lists = splitting._group_alerts(
        "labels", "foo", [{"annotations": {"foo": "bar"}}]
    )
    assert list_of_alert_lists == [[{"annotations": {"foo": "bar"}}]]


def test_group_alerts(caplog, helpers):
    alerts = [
        {
            "whatever": "fefe",
            "annotations": {
                "target_link": "a",
                "foo": "bar",
            },
        },
        {
            "whatever": "fefe",
            "annotations": {
                "target_link": "a",
                "foo": "bar",
            },
        },
        {
            "whatever": "fefe",
            "annotations": {
                "target_link": "b",
                "foo": "bar",
            },
        },
        {
            "whatever": "fefe",
            "annotations": {
                "foo": "bar",
            },
        },
        {
            "whatever": "fefe",
            "annotations": {
                "foo": "dsds",
            },
        },
    ]

    grouped_alerts = splitting._group_alerts("annotations", "target_link", alerts)
    helpers.print_struct(grouped_alerts, "grouped_alerts")

    assert len(grouped_alerts) == 3

    assert [
        {"whatever": "fefe", "annotations": {"foo": "bar"}},
        {"whatever": "fefe", "annotations": {"foo": "dsds"}},
    ] in grouped_alerts

    assert [
        {"whatever": "fefe", "annotations": {"foo": "bar"}},
        {"whatever": "fefe", "annotations": {"foo": "dsds"}},
    ] in grouped_alerts

    assert [
        {"whatever": "fefe", "annotations": {"target_link": "a", "foo": "bar"}},
        {"whatever": "fefe", "annotations": {"target_link": "a", "foo": "bar"}},
    ] in grouped_alerts


# ==============================================================================


def test_create_data_dict_single_alert(caplog, helpers):
    base = {
        "blabla": "blabladfefef",
        "groupKeys": {
            "fefefe": "fefefwe",
        },
        "group_labels": {"will": "do"},
    }

    alerts = [
        {
            "what": "ever",
            "annotations": {
                "a": "aa",
                "b": "bb",
            },
            "labels": {
                "c": "cc",
                "d": "dd",
            },
        },
    ]

    data = splitting._create_data_dict(base, alerts)
    helpers.print_struct(data, "data")

    assert data["blabla"] == "blabladfefef"
    assert data["groupKeys"] == {"fefefe": "fefefwe"}
    assert data["common_annotations"] == {
        "a": "aa",
        "b": "bb",
    }
    assert data["common_labels"] == {
        "c": "cc",
        "d": "dd",
    }
    assert data["alerts"][0] == {
        "what": "ever",
        "annotations": {
            "a": "aa",
            "b": "bb",
        },
        "labels": {
            "c": "cc",
            "d": "dd",
        },
    }
    assert data["group_labels"] == {}


def test_create_data_dict_two_alerts(caplog, helpers):
    base = {
        "blabla": "blabladfefef",
        "groupKeys": {
            "fefefe": "fefefwe",
        },
        "group_labels": {"hot": "hotv"},
    }

    alerts = [
        {
            "what": "ever",
            "annotations": {
                "red": "redv",
                "blue": "bluev",
                "anno": "foo",
            },
            "labels": {
                "hot": "hotv",
                "cold": "coldv",
            },
        },
        {
            "what": "ever",
            "annotations": {
                "orange": "orangev",
                "green": "greenv",
                "blue": "somethingelse",
                "red": "redv",
                "anno": "foo",
            },
            "labels": {
                "c": "cc",
                "hot": "hotv",
                "d": "dd",
            },
        },
    ]

    data = splitting._create_data_dict(base, alerts)
    helpers.print_struct(data, "data")

    assert data["common_annotations"] == {"anno": "foo", "red": "redv"}
    assert data["common_labels"] == {"hot": "hotv"}
    assert data["group_labels"] == {"hot": "hotv"}


# ==============================================================================


def test_split_by(caplog, helpers):
    data = {
        "receiver": "cisco webex",
        "status": "firing",
        "group_labels": {
            "alertname": "JustATestAlert",
            "namespace": "whatever/promstack",
        },
        "common_labels": {
            "alertname": "JustATestAlert",
            "namespace": "whatever/promstack",
            "severity": "info",
        },
        "common_annotations": {
            "investigate_link": "https://domain.com/grafana/d/fdwTIxFMz/container-intra",
            "summary": "Ratio(Max(Working Set, RSS) / Reservation) [5m Avg] \\u003c 40 %",
            "title": "Memory: Relativ memory usage low",
        },
        "alerts": [
            {
                "labels": {},
                "annotations": {
                    "common": "common",
                },
            },
            {
                "labels": {},
                "annotations": {
                    "common": "common",
                    "whatever": "fefe",
                },
            },
            {
                "labels": {"very": "unique"},
                "annotations": {},
            },
        ],
    }

    datas = splitting.split("annotation", "common", data)
    helpers.print_struct(datas, "datas")

    assert datas[0]["receiver"] == "cisco webex"

    assert datas[0]["group_labels"] == {}
    assert datas[0]["alerts"] == [
        {
            "labels": {"very": "unique"},
            "annotations": {},
        }
    ]
    assert datas[1]["common_annotations"] == {"common": "common"}
    assert datas[0]["common_annotations"] == {}
