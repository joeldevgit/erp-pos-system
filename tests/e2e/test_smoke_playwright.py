"""
Suite E2E con Playwright.

Ejecutar localmente:
    playwright install chromium
    pytest tests/e2e --e2e

Cubre endpoints operativos y contrato público de API v2 desde navegador real.
"""
import pytest

pytestmark = pytest.mark.e2e


def test_health_endpoint_e2e(live_server, page):
    page.goto(f"{live_server.url}/health/")
    assert "ok" in page.text_content("body").lower()


def test_live_endpoint_e2e(live_server, page):
    page.goto(f"{live_server.url}/live/")
    body = page.text_content("body").lower()
    assert "live" in body
    assert "myerpposdj" in body


def test_ready_endpoint_e2e(live_server, page):
    page.goto(f"{live_server.url}/ready/")
    body = page.text_content("body").lower()
    assert "ready" in body
    assert "database" in body
    assert "cache" in body


def test_api_v2_status_e2e(live_server, page):
    page.goto(f"{live_server.url}/api/v2/status/")
    body = page.text_content("body").lower()
    assert "v2" in body
    assert "stable" in body
    assert "productos" in body
