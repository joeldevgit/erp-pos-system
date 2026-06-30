from django.test import TestCase

# Create your tests here.
import pytest


@pytest.mark.django_db
def test_health_check(client):
    response = client.get("/health/")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "myerpposdj"


@pytest.mark.django_db
def test_ready_check(client):
    response = client.get("/ready/")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert data["checks"]["database"] == "ok"
    assert data["checks"]["cache"] == "ok"


@pytest.mark.django_db
def test_prometheus_metrics_endpoint(client):
    response = client.get("/metrics")

    assert response.status_code in {200, 301, 302}


@pytest.mark.django_db
def test_openapi_schema_endpoint(client):
    response = client.get("/api/schema/")

    assert response.status_code == 200
