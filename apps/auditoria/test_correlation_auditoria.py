from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from apps.auditoria.services import registrar_auditoria


def test_registrar_auditoria_guarda_correlation_id_ip_user_agent(db):
    request = RequestFactory(HTTP_X_CORRELATION_ID="cid-123", HTTP_USER_AGENT="pytest-agent").get("/")
    request.user = AnonymousUser()
    request.correlation_id = "cid-123"

    log = registrar_auditoria(
        usuario=request.user,
        accion="CREATE",
        app="productos",
        modelo="Producto",
        descripcion="prueba",
        request=request,
    )

    assert log.correlation_id == "cid-123"
    assert log.request_id == "cid-123"
    assert log.user_agent == "pytest-agent"
    assert log.ip_address == "127.0.0.1"
