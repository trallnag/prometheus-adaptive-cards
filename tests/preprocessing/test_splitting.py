"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import pytest

import prometheus_adaptive_cards.preprocessing.splitting as splitting
from prometheus_adaptive_cards.model import Alert, AlertGroup

# ==============================================================================


@pytest.mark.splitting_group_alerts
def test_group_alerts_single_alert():
    list_of_alert_lists = splitting._group_alerts(
        "annotations", "foo", [Alert.construct(annotations={"foo": "bar"})]
    )

    assert isinstance(list_of_alert_lists[0][0], Alert)
    assert len(list_of_alert_lists) == 1
    assert len(list_of_alert_lists[0]) == 1
    assert list_of_alert_lists[0][0] == Alert.construct(annotations={"foo": "bar"})

    list_of_alert_lists = splitting._group_alerts(
        "labels", "foo", [Alert.construct(labels={"foo": "bar"})]
    )

    assert isinstance(list_of_alert_lists[0][0], Alert)
    assert len(list_of_alert_lists) == 1
    assert len(list_of_alert_lists[0]) == 1
    assert list_of_alert_lists[0][0] == Alert.construct(labels={"foo": "bar"})


@pytest.mark.splitting_group_alerts
def test_group_alerts(helpers):
    alerts = [
        Alert.construct(
            **{
                "whatever": "fefe",
                "annotations": {
                    "target_link": "a",
                    "foo": "bar",
                },
            }
        ),
        Alert.construct(
            **{
                "whatever": "fefe",
                "annotations": {
                    "target_link": "a",
                    "foo": "bar",
                },
            }
        ),
        Alert.construct(
            **{
                "whatever": "fefe",
                "annotations": {
                    "target_link": "b",
                    "foo": "bar",
                },
            }
        ),
        Alert.construct(
            **{
                "whatever": "fefe",
                "annotations": {
                    "foo": "bar",
                },
            }
        ),
        Alert.construct(
            **{
                "whatever": "fefe",
                "annotations": {
                    "foo": "dsds",
                },
            }
        ),
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

    assert isinstance(grouped_alerts[0][0], Alert)


# ==============================================================================


@pytest.mark.splitting_create_alert_group
def test_create_alert_group_single_alert(helpers):
    base = AlertGroup.construct(
        **{
            "blabla": "blabladfefef",
            "groupKeys": {
                "fefefe": "fefefwe",
            },
            "group_labels": {"will": "do"},
        }
    )

    alerts = [
        Alert.construct(
            **{
                "what": "ever",
                "annotations": {
                    "a": "aa",
                    "b": "bb",
                },
                "labels": {},
            }
        ),
        Alert.construct(
            **{
                "annotations": {
                    "a": "aa",
                    "b": "bb",
                },
                "labels": {
                    "c": "cc",
                    "d": "dd",
                },
            }
        ),
    ]

    alert_group = splitting._create_alert_group(base, alerts)
    helpers.print_struct(alert_group, "data")

    assert alert_group.blabla == "blabladfefef"
    assert alert_group.groupKeys == {"fefefe": "fefefwe"}
    assert alert_group.common_annotations == {
        "a": "aa",
        "b": "bb",
    }
    assert alert_group.common_labels == {}
    assert alert_group.alerts[0] == {
        "what": "ever",
        "annotations": {
            "a": "aa",
            "b": "bb",
        },
        "labels": {},
    }
    assert alert_group.group_labels == {}


@pytest.mark.splitting_create_alert_group
def test_create_data_dict_two_alerts(caplog, helpers):
    base = AlertGroup.construct(
        **{
            "blabla": "blabladfefef",
            "groupKeys": {
                "fefefe": "fefefwe",
            },
            "group_labels": {"hot": "hotv"},
        }
    )

    alerts = [
        Alert.construct(
            **{
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
            }
        ),
        Alert.construct(
            **{
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
            }
        ),
    ]

    alert_group = splitting._create_alert_group(base, alerts)
    helpers.print_struct(alert_group, "alert_group")

    assert alert_group.common_annotations == {"anno": "foo", "red": "redv"}
    assert alert_group.common_labels == {"hot": "hotv"}
    assert alert_group.group_labels == {"hot": "hotv"}


# ==============================================================================


@pytest.mark.splitting_split
def test_split(caplog, helpers):
    alert_group = AlertGroup.construct(
        **{
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
                Alert.construct(
                    **{
                        "labels": {},
                        "annotations": {
                            "common": "common",
                        },
                    }
                ),
                Alert.construct(
                    **{
                        "labels": {},
                        "annotations": {
                            "common": "common",
                            "whatever": "fefe",
                        },
                    }
                ),
                Alert.construct(
                    **{
                        "labels": {"very": "unique"},
                        "annotations": {},
                    }
                ),
            ],
        }
    )

    alert_groups = splitting.split("annotation", "common", alert_group)
    helpers.print_struct(alert_groups, "alert_groups")

    assert alert_groups[0].receiver == "cisco webex"

    assert alert_groups[0].group_labels == {}
    assert alert_groups[0].alerts == [
        Alert.construct(
            **{
                "labels": {"very": "unique"},
                "annotations": {},
            }
        )
    ]
    assert alert_groups[1].common_annotations == {"common": "common"}
    assert alert_groups[0].common_annotations == {}
