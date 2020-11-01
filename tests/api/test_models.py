"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

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

    assert len(data.alerts) == 2
