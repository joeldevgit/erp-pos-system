from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import TemplateView

from apps.core.views import health_check, live_check, ready_check
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView



urlpatterns = [

    path('', include('django_prometheus.urls')),

    path('admin/', admin.site.urls),

    path("usuarios/", include("apps.usuarios.urls")),

    path("", include("apps.inicio.urls")),

    path("inventario/", include("apps.inventario.urls")),

    path("productos/", include("apps.productos.urls")),
    path("api/v1/", include("apps.api.v1.urls")),
    path("api/v2/", include("apps.api.v2.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    path('serviceworker.js', TemplateView.as_view(template_name="serviceworker.js", content_type='application/javascript')),


    path("health/", health_check),
    path("live/", live_check),
    path("ready/", ready_check),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)