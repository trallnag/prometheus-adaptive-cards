"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

import pytest
import requests_mock

from prometheus_adaptive_cards.config import Sending, Target
from prometheus_adaptive_cards.distribution import Payload, distribution

# ==============================================================================


@pytest.mark.slow
def test_handle_send_failure_as_get_to_url_successful():
    with requests_mock.Mocker() as mocker:
        mocker.get("http://www.test.com", text="hallo", status_code=200)
        response = distribution._handle_send_failure(
            error_payload=None,
            url="http://www.test.com",
            notify_url=None,
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
            notify_url=None,
        )
        assert response.status_code == 405
        assert response.request.method == "GET"


@pytest.mark.slow
def test_handle_send_failure_as_get_to_notify_url_successful():
    with requests_mock.Mocker() as mocker:
        mocker.get("http://www.fupa.com", text="hallo", status_code=199)
        response = distribution._handle_send_failure(
            error_payload=None,
            url="http://www.test.com",
            notify_url="http://www.fupa.com",
        )
        assert response.status_code == 199
        assert response.request.method == "GET"


@pytest.mark.slow
def test_handle_send_failure_as_get_to_notify_url_unsuccessful():
    with requests_mock.Mocker() as mocker:
        mocker.get("http://www.fupa.com", text="hallo", status_code=499)
        response = distribution._handle_send_failure(
            error_payload=None,
            url="http://www.test.com",
            notify_url="http://www.fupa.com",
        )
        assert response.status_code == 499
        assert response.request.method == "GET"


@pytest.mark.slow
def test_handle_send_failure_as_post_to_notify_url_successful():
    with requests_mock.Mocker() as mocker:
        mocker.post("http://www.fupa.com", text="hallo", status_code=199)
        response = distribution._handle_send_failure(
            error_payload={"wup": "die"},
            url="http://www.test.com",
            notify_url="http://www.fupa.com",
        )
        assert response.status_code == 199
        assert response.request.method == "POST"


# ==============================================================================


URL1 = "http://www.url1.com/"
URL2 = "http://www.url2.com/"
notify_url = "http://www.notify_url.com/"
SENDING = Sending(notify_url=notify_url)
TARGET1 = Target(url=URL1)
TARGET2 = Target(url=URL2)
PAYLOAD = Payload(data={"hello": "world"}, targets=[TARGET1, TARGET2])


def error_parser(dct: dict) -> dict:
    return {"message": "error"}


@pytest.mark.slow
def test_send_no_target():
    payload = Payload(
        data={"hello": "world"},
        targets=[Target()],
    )
    responses = distribution.send([payload], SENDING, error_parser)
    assert len(responses) == 0


@pytest.mark.slow
def test_send_single_payload_successfully():
    with requests_mock.Mocker() as mocker:
        mocker.post(URL1, text="hallo", status_code=200)
        mocker.post(URL2, text="hallo", status_code=200)
        responses = distribution.send([PAYLOAD], SENDING, error_parser)
        assert len(responses) == 2
        assert responses[0].request.url == URL1
        assert responses[1].request.url == URL2
        assert responses[0].status_code == 200
        assert responses[1].status_code == 200


@pytest.mark.slow
def test_send_multiple_payloads_successfully():
    with requests_mock.Mocker() as mocker:
        mocker.post(URL1, text="hallo", status_code=200)
        mocker.post(URL2, text="hallo", status_code=200)
        responses = distribution.send([PAYLOAD, PAYLOAD], SENDING, error_parser)
        assert len(responses) == 4
        assert responses[0].request.url == URL1
        assert responses[1].request.url == URL2
        assert responses[0].status_code == 200
        assert responses[1].status_code == 200


@pytest.mark.slow
def test_send_fail_with_error_parser_successful():
    with requests_mock.Mocker() as mocker:
        mocker.post(URL1, text="hallo", status_code=404)
        mocker.post(URL2, text="hallo", status_code=404)
        mocker.post(notify_url, text="x", status_code=200)
        responses = distribution.send([PAYLOAD], SENDING, error_parser)
        assert len(responses) == 4
        assert responses[0].status_code == 404
        assert responses[1].status_code == 200
        assert responses[2].status_code == 404
        assert responses[3].status_code == 200


@pytest.mark.slow
def test_send_fail_without_error_parser():
    with requests_mock.Mocker() as mocker:
        mocker.post(URL1, text="hallo", status_code=404)
        mocker.post(URL2, text="hallo", status_code=404)
        mocker.get(notify_url, text="x", status_code=200)
        responses = distribution.send([PAYLOAD], SENDING)
        assert len(responses) == 4
        assert responses[0].status_code == 404
        assert responses[1].status_code == 200
        assert responses[2].status_code == 404
        assert responses[3].status_code == 200


# ==============================================================================
