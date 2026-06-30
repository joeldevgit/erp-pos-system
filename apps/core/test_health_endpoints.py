import pytest


@pytest.mark.django_db
def test_health_live_ready_endpoints(client):
    health = client.get("/health/")
    live = client.get("/live/")
    ready = client.get("/ready/")

    assert health.status_code == 200
    assert health.json()["status"] == "ok"
    assert live.status_code == 200
    assert live.json()["status"] == "live"
    assert ready.status_code == 200
    assert ready.json()["status"] == "ready"
    assert ready.json()["checks"]["database"] == "ok"
    assert ready.json()["checks"]["cache"] == "ok"
