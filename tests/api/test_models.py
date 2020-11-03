"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import copy
import json
import os
from datetime import datetime, timedelta, timezone

from prometheus_adaptive_cards.api.models import Alert, Data


def test_alert_based_on_example():
    alert = Alert(**Alert.Config.schema_extra["example"])

    # Ensure that aliasing is working.
    assert hasattr(alert, "fingerprint")
    assert hasattr(alert, "starts_at")
    assert not hasattr(alert, "startsAt")
    assert hasattr(alert, "generator_url")
    assert not hasattr(alert, "generatorURL")

    # Ensure correct datetime conversion from string.
    assert type(alert.starts_at) == datetime
    assert abs(
        alert.starts_at - datetime(2020, 10, 11, 14, 34, 11, tzinfo=timezone.utc)
    ) < timedelta(seconds=1)


def test_data_based_on_example():
    data = Data(**Data.Config.schema_extra["example"])

    # Ensure that aliasing is working.
    assert hasattr(data, "receiver")
    assert hasattr(data, "alerts")
    assert hasattr(data, "group_key")
    assert not hasattr(data, "groupKey")
    assert hasattr(data, "common_annotations")
    assert not hasattr(data, "commonAnnotations")
    assert hasattr(data, "truncated_alerts")

    assert len(data.alerts) == 2


def test_data_based_on_example_optionals():
    payload = copy.deepcopy(Data.Config.schema_extra["example"])
    del payload["truncatedAlerts"]
    data = Data(**payload)

    assert data.truncated_alerts == 0


def test_data_based_on_data_payload_simple_01():
    with open(f"{os.path.dirname(__file__)}/data/payload-simple-01.json") as file:
        data = Data(**json.load(file))
        assert data.receiver == "generic"
        assert data.status == "firing"
        assert data.external_url == "http://1217896f2a1d:9093"
        assert data.version == "4"
        assert data.group_key == '{}:{alertname="WhatEver"}'
        assert data.truncated_alerts == 0
        assert data.group_labels == {"alertname": "WhatEver"}
        assert data.common_labels == {
            "alertname": "WhatEver",
            "foo_bar_qux": "foo_moo_zoom",
            "severity": "warning",
        }
        assert data.common_annotations == {
            "description": "A Prometheus job has disappeared\\n  VALUE = 2\\n  LABELS: map[]",
            "summary": "Prometheus job missing (instance )",
        }
        assert data.alerts[0].status == "firing"
