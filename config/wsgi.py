import os
from django.core.wsgi import get_wsgi_application

# Usa variable de entorno, por defecto local
# Mejora: permite elegir el entorno desde variable de entorno
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    os.getenv('DJANGO_SETTINGS_MODULE', 'config.settings.local')
)

application = get_wsgi_application()