"""Copyright © 2020 Tim Schwenke - Licensed under the Apache License 2.0"""

from fastapi.testclient import TestClient

from prometheus_adaptive_cards.api.app import create_fastapi_base


def test_route_health():
    client = TestClient(create_fastapi_base())
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "OK", "symbol": "👌"}
