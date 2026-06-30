# Observabilidad

## Swagger / OpenAPI

La documentación interactiva de la API queda disponible en:

```text
/api/docs/
/api/redoc/
/api/schema/
```

La configuración está en `REST_FRAMEWORK` y `SPECTACULAR_SETTINGS` dentro de `config/settings/base.py`.

## Health checks

Endpoints operativos:

```text
/health/   -> confirma que Django está vivo
/ready/    -> valida base de datos y cache
```

`/ready/` responde `503` si alguna dependencia crítica falla.

## Prometheus Metrics

`django-prometheus` expone métricas en:

```text
/metrics
```

El middleware Prometheus está activado al inicio y final del stack de middleware.

## Sentry

En producción se activa con:

```bash
SENTRY_DSN=https://...
```

La integración está en `config/settings/production.py` con `sentry_sdk.init()`.

## Coverage obligatorio

La cobertura se mide con:

```bash
pytest --cov=apps --cov-config=.coveragerc --cov-report=term-missing --cov-fail-under=90
```

El CI de GitHub falla automáticamente si baja de 90%.
