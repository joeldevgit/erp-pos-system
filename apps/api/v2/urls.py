from django.urls import include, path
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView

from apps.api.views import (
    AlmacenViewSet,
    CategoriaViewSet,
    MovimientoProductoViewSet,
    ProductoViewSet,
    StockProductoViewSet,
    UnidadViewSet,
)


class APIV2StatusView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({
            "version": "v2",
            "status": "stable",
            "message": "API v2 disponible; mantiene recursos principales y deja espacio para contratos nuevos.",
            "resources": ["productos", "categorias", "unidades", "almacenes", "stocks", "movimientos"],
        })


router = DefaultRouter()
router.register("productos", ProductoViewSet, basename="api-v2-productos")
router.register("categorias", CategoriaViewSet, basename="api-v2-categorias")
router.register("unidades", UnidadViewSet, basename="api-v2-unidades")
router.register("almacenes", AlmacenViewSet, basename="api-v2-almacenes")
router.register("stocks", StockProductoViewSet, basename="api-v2-stocks")
router.register("movimientos", MovimientoProductoViewSet, basename="api-v2-movimientos")

urlpatterns = [
    path("status/", APIV2StatusView.as_view(), name="api-v2-status"),
    path("", include(router.urls)),
]
