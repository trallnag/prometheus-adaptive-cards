"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""


import prometheus_adaptive_cards.preprocessing.enhancement as enhancement
from prometheus_adaptive_cards.api.models import Data


def test_enhance_data_request_object():
    data = Data(**Data.Config.schema_extra["example"])

    data = enhancement.enhance_data(None, data)

    assert data.request is None


def test_enhance_specific_annotations(helpers):
    data = Data(**Data.Config.schema_extra["example"])
    data.alerts[0].annotations.update(
        {"specific": "specific", "very_specific": "very_specific"}
    )

    data = enhancement.enhance_data("", data)

    assert data.alerts[0].specific_annotations["specific"] == "specific"
    assert hasattr(data.alerts[0], "specific_annotations")
    assert hasattr(data.alerts[1], "specific_annotations")
    assert hasattr(data.alerts[0], "specific_labels")
    assert hasattr(data.alerts[1], "specific_labels")


def test_enhance_specific_labels(helpers):
    data = Data(**Data.Config.schema_extra["example"])
    data.alerts[0].labels.update(
        {"specific": "specific", "very_specific": "very_specific"}
    )

    data = enhancement.enhance_data("", data)

    assert data.alerts[0].specific_labels["specific"] == "specific"
    assert hasattr(data.alerts[0], "specific_labels")
    assert hasattr(data.alerts[1], "specific_labels")
