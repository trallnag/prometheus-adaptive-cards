"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

from prometheus_adaptive_cards.distribution import distribution
import requests_mock
import pytest

# ==============================================================================


@pytest.mark.slow
def test_handle_send_failure_as_get_to_url_successful():
    with requests_mock.Mocker() as mocker:
        mocker.get("http://www.test.com", text="hallo", status_code=200)
        response = distribution._handle_send_failure(
            error_payload=None,
            url="http://www.test.com",
            fallback_url=None,
        )
        assert response.status_code == 200
        assert response.request.method == "GET"


@pytest.mark.slow
def test_handle_send_failure_as_get_to_url_unsuccessful():
    with requests_mock.Mocker() as mocker:
        mocker.get("http://www.test.com", text="hallo", status_code=405)
        response = distribution._handle_send_failure(
            error_payload=None,
            url="http://www.test.com",
            fallback_url=None,
        )
        assert response.status_code == 405
        assert response.request.method == "GET"


@pytest.mark.slow
def test_handle_send_failure_as_get_to_fallback_url_successful():
    with requests_mock.Mocker() as mocker:
        mocker.get("http://www.fupa.com", text="hallo", status_code=199)
        response = distribution._handle_send_failure(
            error_payload=None,
            url="http://www.test.com",
            fallback_url="http://www.fupa.com",
        )
        assert response.status_code == 199
        assert response.request.method == "GET"


@pytest.mark.slow
def test_handle_send_failure_as_get_to_fallback_url_unsuccessful():
    with requests_mock.Mocker() as mocker:
        mocker.get("http://www.fupa.com", text="hallo", status_code=499)
        response = distribution._handle_send_failure(
            error_payload=None,
            url="http://www.test.com",
            fallback_url="http://www.fupa.com",
        )
        assert response.status_code == 499
        assert response.request.method == "GET"


@pytest.mark.slow
def test_handle_send_failure_as_post_to_fallback_url_successful():
    with requests_mock.Mocker() as mocker:
        mocker.post("http://www.fupa.com", text="hallo", status_code=199)
        response = distribution._handle_send_failure(
            error_payload={"wup": "die"},
            url="http://www.test.com",
            fallback_url="http://www.fupa.com",
        )
        assert response.status_code == 199
        assert response.request.method == "POST"


# ==============================================================================
