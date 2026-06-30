from django.http import JsonResponse
from django.db import connection


def health_check(request):
    return JsonResponse({"status": "ok"})


def ready_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return JsonResponse({"status": "ready"})
    except Exception:
        return JsonResponse({"status": "error"}, status=500)
from django.core.cache import cache
from django.db import connection
from django.http import JsonResponse


SERVICE_NAME = "myerpposdj"


def health_check(request):
    """Health general para monitoreo externo."""
    return JsonResponse({"status": "ok", "service": SERVICE_NAME})


def live_check(request):
    """Liveness: confirma que el proceso Django está vivo."""
    return JsonResponse({"status": "live", "service": SERVICE_NAME})


def ready_check(request):
    """Readiness: valida dependencias mínimas para servir tráfico."""
    checks = {
        "database": "unknown",
        "cache": "unknown",
    }
    status_code = 200

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        checks["database"] = "ok"
    except Exception as exc:  # pragma: no cover
        checks["database"] = f"error: {exc.__class__.__name__}"
        status_code = 503

    try:
        cache.set("healthcheck", "ok", timeout=10)
        checks["cache"] = "ok" if cache.get("healthcheck") == "ok" else "error"
        if checks["cache"] != "ok":
            status_code = 503
    except Exception as exc:  # pragma: no cover
        checks["cache"] = f"error: {exc.__class__.__name__}"
        status_code = 503

    return JsonResponse(
        {
            "status": "ready" if status_code == 200 else "error",
            "service": SERVICE_NAME,
            "checks": checks,
        },
        status=status_code,
    )
