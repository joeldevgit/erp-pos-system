from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AlmacenViewSet,
    CategoriaViewSet,
    MovimientoProductoViewSet,
    ProductoViewSet,
    StockProductoViewSet,
    UnidadViewSet,
)

router = DefaultRouter()
router.register("productos", ProductoViewSet, basename="api-productos")
router.register("categorias", CategoriaViewSet, basename="api-categorias")
router.register("unidades", UnidadViewSet, basename="api-unidades")
router.register("almacenes", AlmacenViewSet, basename="api-almacenes")
router.register("stocks", StockProductoViewSet, basename="api-stocks")
router.register("movimientos", MovimientoProductoViewSet, basename="api-movimientos")

urlpatterns = [path("", include(router.urls))]
