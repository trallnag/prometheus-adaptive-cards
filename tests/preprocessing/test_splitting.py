"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import prometheus_adaptive_cards.preprocessing.splitting as splitting


# ==============================================================================


def test_group_alerts_single_alert(caplog):
    list_of_alert_lists = splitting.group_alerts(
        "annotations", "foo", [{"annotations": {"foo": "bar"}}]
    )
    assert list_of_alert_lists == [[{"annotations": {"foo": "bar"}}]]

    list_of_alert_lists = splitting.group_alerts(
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

    grouped_alerts = splitting.group_alerts("annotations", "target_link", alerts)
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