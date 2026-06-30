from .base import *
import os
import dj_database_url
import sentry_sdk

# ============================================================
# AMBIENTE
# ============================================================
DEBUG = False
ENVIRONMENT = 'production'

# ============================================================
# HOSTS PERMITIDOS
# ============================================================
ALLOWED_HOSTS = [
    "pos-django-zrzo.onrender.com",
    ".onrender.com",
]

# ============================================================
# STATIC FILES - PRODUCCIÓN CON WHITENOISE
# ============================================================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)

# ============================================================
# MEDIA FILES
# ============================================================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ============================================================
# SEGURIDAD EN PRODUCCIÓN
# ============================================================
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ============================================================
# BASE DE DATOS EN PRODUCCIÓN
# ============================================================
# BASE DE DATOS EN PRODUCCIÓN - POSTGRESQL
# ============================================================
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL es obligatoria en producción. Usa PostgreSQL.")

DATABASES = {
    "default": dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# ============================================================
# CACHE EN PRODUCCIÓN - REDIS
# ============================================================
REDIS_URL = os.getenv("REDIS_URL")
if REDIS_URL:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        }
    }

# ============================================================
# LOGS EN PRODUCCIÓN
# ============================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}


SENTRY_DSN = os.getenv("SENTRY_DSN")

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        traces_sample_rate=0.2,
        send_default_pii=False,
    )

# ============================================================
# CABECERAS Y COOKIES SEGURAS
# ============================================================
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
X_FRAME_OPTIONS = "DENY"
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "https://*.onrender.com").split(",") if origin.strip()]

# API en producción: límites más estrictos.
REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"] = {
    "user": os.getenv("DRF_USER_THROTTLE", "2000/day"),
    "anon": os.getenv("DRF_ANON_THROTTLE", "60/day"),
}
