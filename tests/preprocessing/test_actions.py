"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import re

import prometheus_adaptive_cards.preprocessing.actions as actions
from prometheus_adaptive_cards.api.models import Data

# ==============================================================================


def test_remove_annotations():
    data = Data(**Data.Config.schema_extra["example"])

    assert "investigate_link" in data.common_annotations
    assert "summary" in data.common_annotations

    actions._remove("annotations", ["investigate_link", "summary"], data)

    assert "investigate_link" not in data.common_annotations
    assert "summary" not in data.common_annotations

    for alert in data.alerts:
        assert "investigate_link" not in alert.annotations
        assert "summary" not in alert.annotations

    data = Data(**Data.Config.schema_extra["example"])

    assert "investigate_link" in data.common_annotations
    assert "summary" in data.common_annotations


def test_remove_labels():
    data = Data(**Data.Config.schema_extra["example"])

    assert "alertname" in data.common_labels
    assert "namespace" in data.common_labels

    actions._remove("labels", ["alertname", "namespace"], data)

    assert "alertname" not in data.common_labels
    assert "namespace" not in data.common_labels

    for alert in data.alerts:
        assert "alertname" not in alert.labels
        assert "namespace" not in alert.labels

    data = Data(**Data.Config.schema_extra["example"])

    assert "alertname" in data.common_labels
    assert "namespace" in data.common_labels


# ==============================================================================


def test_remove_re_annotations_simple():
    data = Data(**Data.Config.schema_extra["example"])

    assert "investigate_link" in data.common_annotations
    assert "summary" in data.common_annotations

    actions._remove_re(
        "annotations", [re.compile("^investigat.*$"), re.compile("^summary$")], data
    )

    assert "investigate_link" not in data.common_annotations
    assert "summary" not in data.common_annotations

    for alert in data.alerts:
        assert "investigate_link" not in alert.annotations
        assert "summary" not in alert.annotations

    data = Data(**Data.Config.schema_extra["example"])

    assert "investigate_link" in data.common_annotations
    assert "summary" in data.common_annotations


def test_remove_re_annotations_extended():
    data = Data(**Data.Config.schema_extra["example"])
    data.common_annotations.update(
        {
            "__whatever": "fefefew",
            "__zoomi": "fefefew",
            "fefe__fefe": "123",
        }
    )

    actions._remove_re("annotations", [re.compile("^__.*$")], data)

    assert "__whatever" not in data.common_annotations
    assert "__zoomi" not in data.common_annotations
    assert "fefe__fefe" in data.common_annotations


# ==============================================================================


def test_add_annotations_everywhere():
    data = Data(**Data.Config.schema_extra["example"])

    assert len(data.common_annotations) == 3

    actions._add("annotations", {"new2": "foo", "ogo": "bar"}, data)

    assert len(data.common_annotations) == 5
    assert data.common_annotations["new2"] == "foo"
    assert data.common_annotations["ogo"] == "bar"

    for alert in data.alerts:
        assert alert.annotations["new2"] == "foo"
        assert alert.annotations["ogo"] == "bar"


def test_add_labels_everywhere():
    data = Data(**Data.Config.schema_extra["example"])

    assert len(data.common_labels) == 3

    actions._add("labels", {"new2": "foo", "ogo": "bar"}, data)

    assert len(data.common_labels) == 5
    assert data.common_labels["new2"] == "foo"
    assert data.common_labels["ogo"] == "bar"

    for alert in data.alerts:
        assert alert.labels["new2"] == "foo"
        assert alert.labels["ogo"] == "bar"


def test_add_annotations_partly_common():
    data = Data(**Data.Config.schema_extra["example"])
    data.alerts[0].annotations.update({"foo": "bar"})

    actions._add("annotations", {"foo": "bar"}, data)

    assert data.common_annotations["foo"] == "bar"

    for alert in data.alerts:
        assert alert.annotations["foo"] == "bar"


def test_add_labels_partly_common():
    data = Data(**Data.Config.schema_extra["example"])
    data.alerts[0].labels.update({"foo": "bar"})

    actions._add("labels", {"foo": "bar"}, data)

    assert data.common_labels["foo"] == "bar"

    for alert in data.alerts:
        assert alert.labels["foo"] == "bar"


def test_add_annotations_partly_uncommon():
    data = Data(**Data.Config.schema_extra["example"])
    data.alerts[0].annotations.update({"foo": "bar"})

    actions._add("annotations", {"foo": "zoom"}, data)

    assert data.common_annotations.get("foo") is None
    assert data.alerts[0].annotations.get("foo") == "bar"
    assert data.alerts[1].annotations.get("foo") == "zoom"


def test_add_labels_partly_uncommon():
    data = Data(**Data.Config.schema_extra["example"])
    data.alerts[0].labels.update({"foo": "bar"})

    actions._add("labels", {"foo": "zoom"}, data)

    assert data.common_labels.get("foo") is None
    assert data.alerts[0].labels.get("foo") == "bar"
    assert data.alerts[1].labels.get("foo") == "zoom"


# ==============================================================================


def test_override_annotations_partly_uncommon():
    data = Data(**Data.Config.schema_extra["example"])
    data.alerts[0].annotations.update({"foo": "bar"})

    actions._override("annotations", {"foo": "zoom"}, data)

    assert data.common_annotations.get("foo") == "zoom"
    assert data.alerts[0].annotations.get("foo") == "zoom"
    assert data.alerts[1].annotations.get("foo") == "zoom"


def test_override_labels_partly_uncommon():
    data = Data(**Data.Config.schema_extra["example"])
    data.alerts[0].labels.update({"foo": "bar"})

    actions._override("labels", {"foo": "zoom"}, data)

    assert data.common_labels.get("foo") == "zoom"
    assert data.alerts[0].labels.get("foo") == "zoom"
    assert data.alerts[1].labels.get("foo") == "zoom"


# ==============================================================================
