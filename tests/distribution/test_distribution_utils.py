"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import time

import pytest
import requests

from prometheus_adaptive_cards.config.settings import Target
from prometheus_adaptive_cards.distribution import utils

# ==============================================================================


@pytest.mark.slow
def test_requests_retry_session():
    s = requests.Session()
    s.auth = ("user", "pass")
    s.headers.update({"x-test": "true"})

    t0 = time.time()

    try:
        _ = utils.requests_retry_session(session=s, retries=3, backoff_factor=0.05).get("http://localhost:9999")
    except Exception as x:
        print('It failed :(', x.__class__.__name__)

    t1 = time.time()

    assert t1 - t0 >= 0.1


# ==============================================================================


def test_extract_url_expansion_url_valid():
    url = utils.extract_url(
        target=Target.construct(expansion_url="hallo/{common_labels[namespace]}/fefe"),
        common_labels={"namespace": "hallo"},
    )
    assert url == "hallo/hallo/fefe"


def test_extract_url_expansion_url_invalid():
    url = utils.extract_url(
        target=Target.construct(expansion_url="hallo/{commond_labels[namespace]}/fefe"),
        common_labels={"namespace": "hallo"},
    )
    assert url is None


def test_extract_url_from_label_valid():
    url = utils.extract_url(
        target=Target.construct(url="does not matter", url_from_label="pickme"),
        common_labels={"pickme": "hallo"},
    )
    assert url == "hallo"


def test_extract_url_from_label_invalid():
    url = utils.extract_url(
        target=Target.construct(url="does not matter", url_from_label="doesnotexist"),
        common_labels={"pickme": "hallo"},
    )
    assert url == "does not matter"


def test_extract_url_from_annotation_valid():
    url = utils.extract_url(
        target=Target.construct(url="does not matter", url_from_annotation="pickme"),
        common_annotations={"pickme": "hallo"},
    )
    assert url == "hallo"


def test_extract_url_from_annotation_invalid():
    url = utils.extract_url(
        target=Target.construct(
            url="does not matter", url_from_annotation="doesnotexist"
        ),
        common_annotations={"pickme": "hallo"},
    )
    assert url == "does not matter"


# ==============================================================================
