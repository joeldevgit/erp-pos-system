# Producción Senior

Este proyecto queda preparado para producción con:

## PostgreSQL
Variable obligatoria en producción:

```bash
DATABASE_URL=postgres://USER:PASSWORD@HOST:5432/DB_NAME
```

En `config/settings/production.py` se exige `DATABASE_URL`; si no existe, Django no inicia. Esto evita usar SQLite accidentalmente en producción.

## Redis
Variable recomendada:

```bash
REDIS_URL=redis://HOST:6379/1
```

Redis queda conectado como backend de cache con `django-redis`.

## DRF
Endpoints base:

```text
/api/v1/productos/
/api/v1/categorias/
/api/v1/unidades/
/api/v1/almacenes/
/api/v1/stocks/
/api/v1/movimientos/
```

La API usa autenticación de sesión/basic y permisos `IsAuthenticated`.

## Cobertura >90%

```bash
pytest --cov=apps --cov-report=term-missing --cov-fail-under=90
```

El workflow de GitHub falla si la cobertura baja de 90%.

## Sentry + métricas

Sentry se activa con:

```bash
SENTRY_DSN=https://...
```

Métricas Prometheus disponibles en:

```text
/metrics
```

## Deploy automático

El workflow `.github/workflows/deploy-render.yml` dispara un deploy de Render solo si las pruebas pasan.

Configura en GitHub Secrets:

```text
RENDER_DEPLOY_HOOK_URL
```


## Health checks

```text
/health/ -> liveness
/ready/  -> readiness con database y cache
```

## Swagger / OpenAPI

```text
/api/schema/
/api/docs/
/api/redoc/
```

## Coverage real actual

Última ejecución local validada:

```text
28 passed
Total coverage: 93.03%
```
