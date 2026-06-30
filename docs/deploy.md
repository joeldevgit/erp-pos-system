# Deploy

## Entorno recomendado

- Python 3.12
- PostgreSQL
- Redis
- Gunicorn
- WhiteNoise
- Sentry

## Variables obligatorias

```bash
DJANGO_SETTINGS_MODULE=config.settings.production
SECRET_KEY=...
DATABASE_URL=postgres://USER:PASSWORD@HOST:5432/DB
ALLOWED_HOSTS=midominio.com,.onrender.com
CSRF_TRUSTED_ORIGINS=https://midominio.com,https://*.onrender.com
```

## Variables recomendadas

```bash
REDIS_URL=redis://HOST:6379/1
SENTRY_DSN=https://...
DRF_USER_THROTTLE=2000/day
DRF_ANON_THROTTLE=60/day
```

## Comandos

```bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn config.wsgi:application
```

## Healthchecks

- `/health/`: aplicación viva.
- `/ready/`: conexión a base de datos lista.
- `/metrics/`: métricas Prometheus por `django-prometheus`.

## Rollback

Mantener releases versionados en Git. Si falla deploy, volver al commit anterior y ejecutar migraciones reversibles solo si fueron diseñadas para rollback.
