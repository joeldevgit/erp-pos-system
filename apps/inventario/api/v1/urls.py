from rest_framework.routers import DefaultRouter

from .views import (
    AlmacenViewSet,
    MermaProductoViewSet,
    MovimientoProductoViewSet,
    StockProductoViewSet,
)

router = DefaultRouter()
router.register("almacenes", AlmacenViewSet, basename="inventario-almacenes")
router.register("stock", StockProductoViewSet, basename="inventario-stock")
router.register("movimientos", MovimientoProductoViewSet, basename="inventario-movimientos")
router.register("mermas", MermaProductoViewSet, basename="inventario-mermas")

urlpatterns = router.urls
