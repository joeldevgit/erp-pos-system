from .models import AuditLog
from apps.core.correlation import get_correlation_id


def _get_client_ip(request):
    if not request:
        return None

    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR")


def registrar_auditoria(
    *,
    usuario=None,
    accion,
    app,
    modelo,
    objeto_id=None,
    descripcion="",
    request=None,
    correlation_id=None,
):
    cid = (
        correlation_id
        or getattr(request, "correlation_id", None)
        or get_correlation_id()
        or ""
    )

    return AuditLog.objects.create(
        usuario=usuario if usuario and usuario.is_authenticated else None,
        accion=accion,
        app=app,
        modelo=modelo,
        objeto_id=objeto_id,
        descripcion=descripcion,
        correlation_id=cid,
        request_id=cid,
        ip_address=_get_client_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", "") if request else "",
    )