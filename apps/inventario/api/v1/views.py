from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.inventario.models import Almacen, MermaProducto, MovimientoProducto, StockProducto
from .serializers import (
    AlmacenSerializer,
    MermaProductoSerializer,
    MovimientoProductoSerializer,
    StockProductoSerializer,
)


class AlmacenViewSet(ReadOnlyModelViewSet):
    queryset = Almacen.objects.all().order_by("nombre")
    serializer_class = AlmacenSerializer


class StockProductoViewSet(ReadOnlyModelViewSet):
    queryset = StockProducto.objects.select_related("producto", "almacen").all()
    serializer_class = StockProductoSerializer


class MovimientoProductoViewSet(ReadOnlyModelViewSet):
    queryset = MovimientoProducto.objects.select_related("producto", "almacen").order_by("-fecha")
    serializer_class = MovimientoProductoSerializer


class MermaProductoViewSet(ReadOnlyModelViewSet):
    queryset = MermaProducto.objects.select_related("producto").order_by("-fecha")
    serializer_class = MermaProductoSerializer
