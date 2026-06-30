from pathlib import Path
import os
from django.core.management.utils import get_random_secret_key
import dj_database_url


BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ============================================================
# SECRET KEY - MEJORADO CON SEGURIDAD
# ============================================================
SECRET_KEY = os.environ.get("SECRET_KEY")

# En producción, si no hay SECRET_KEY, lanza error
if not SECRET_KEY:
    if os.getenv('ENVIRONMENT') == 'production':
        raise ValueError(
            "❌ ERROR CRÍTICO: SECRET_KEY no está configurada en producción. "
            "Debes establecer la variable de entorno SECRET_KEY."
        )
    # En desarrollo, genera una automáticamente
    SECRET_KEY = get_random_secret_key()

# ============================================================
# DEBUG - MEJORADO
# ============================================================
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# ============================================================
# ALLOWED HOSTS - MEJORADO
# ============================================================
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS]







# APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_prometheus',
    'rest_framework',
    'django_filters',
    'drf_spectacular',
    'widget_tweaks',

    'apps.inicio',
    'apps.productos',
    'apps.inventario',
    'apps.usuarios',

    'apps.api',

    "apps.auditoria.apps.AuditoriaConfig",
    "apps.core",
]

# MIDDLEWARE
MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'apps.core.middleware.CorrelationIdMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← Agrega esta para estilos css, js

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

# URLS
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'config.context_processors.navbar_context',
            ],
        },
    },
]




# DATABASE
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# API REST
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.AnonRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "user": os.getenv("DRF_USER_THROTTLE", "1000/day"),
        "anon": os.getenv("DRF_ANON_THROTTLE", "100/day"),
    },
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": int(os.getenv("API_PAGE_SIZE", "20")),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "MyERPPosDJ API",
    "DESCRIPTION": "API pública versionada del ERP/POS. v1 estable; v2 reservada para cambios incompatibles.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
}

API_VERSION = os.getenv("API_VERSION", "v1")

# PASSWORDS
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# LANGUAGE
LANGUAGE_CODE = 'es-pe'
TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_TZ = True

# STATIC FILES
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# MEDIA
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# DEFAULT PK
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# LOGIN
LOGIN_URL = "usuarios:login"
LOGIN_REDIRECT_URL = 'inicio'
LOGOUT_REDIRECT_URL = 'usuarios:login'

# LOGGING
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "simple": {
            "format": "[{levelname}] {asctime} {name}: {message}",
            "style": "{",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },

    "root": {
        "handlers": ["console"],
        "level": "INFO",
 }}

# LOGGING ESTRUCTURADO JSON + CORRELATION ID
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "correlation_id": {
            "()": "apps.core.logging.CorrelationIdFilter",
        },
    },
    "formatters": {
        "json": {
            "()": "apps.core.logging.JsonFormatter",
        },
        "simple": {
            "format": "[{levelname}] {asctime} {name} [{correlation_id}]: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": os.getenv("LOG_FORMAT", "json"),
            "filters": ["correlation_id"],
        },
    },
    "root": {
        "handlers": ["console"],
        "level": os.getenv("LOG_LEVEL", "INFO"),
    },
}



CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_URL", "redis://127.0.0.1:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}
