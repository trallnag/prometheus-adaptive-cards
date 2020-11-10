"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import time

import pytest
import requests
from requests import ConnectionError

from prometheus_adaptive_cards.distribution import utils


@pytest.mark.slow
def test_requests_retry_session():
    s = requests.Session()
    s.auth = ("user", "pass")
    s.headers.update({"x-test": "true"})

    t0 = time.time()
    with pytest.raises(ConnectionError):
        response = utils.requests_retry_session(session=s).get("https://www.peterbe.com")
    t1 = time.time()
    assert t1 - t0 >= 1.8
