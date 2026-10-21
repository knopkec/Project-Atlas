"""Smoke test for the application health endpoint."""

from tests.conftest import client


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
