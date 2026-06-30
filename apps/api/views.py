from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.productos.models import Categoria, Producto, Unidad
from apps.inventario.models import Almacen, StockProducto, MovimientoProducto
from .permissions import RolModuloPermission
from apps.productos.usecases.api_producto_usecase import ProductoAPIUseCase
from .serializers import (
    AlmacenSerializer,
    CategoriaSerializer,
    MovimientoProductoSerializer,
    ProductoSerializer,
    StockProductoSerializer,
    UnidadSerializer,
)


class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = [RolModuloPermission]


class CategoriaViewSet(BaseModelViewSet):
    queryset = Categoria.objects.all().order_by("nombre")
    serializer_class = CategoriaSerializer


class UnidadViewSet(BaseModelViewSet):
    queryset = Unidad.objects.all().order_by("nombre")
    serializer_class = UnidadSerializer


class ProductoViewSet(BaseModelViewSet):
    queryset = Producto.objects.select_related("categoria", "unidad").order_by("-id")
    serializer_class = ProductoSerializer
    filterset_fields = ["estado", "categoria", "unidad"]
    search_fields = ["nombre", "codigo"]
    ordering_fields = ["id", "nombre", "stock", "precio_venta"]

    @action(detail=True, methods=["post"], url_path="cambiar-estado")
    def cambiar_estado(self, request, pk=None):
        producto = self.get_object()
        producto = ProductoAPIUseCase.cambiar_estado(producto, usuario=request.user)
        return Response(self.get_serializer(producto).data)


class AlmacenViewSet(BaseModelViewSet):
    queryset = Almacen.objects.all().order_by("nombre")
    serializer_class = AlmacenSerializer


class StockProductoViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [RolModuloPermission]
    queryset = StockProducto.objects.select_related("producto", "almacen").order_by("producto__nombre")
    serializer_class = StockProductoSerializer


class MovimientoProductoViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [RolModuloPermission]
    queryset = MovimientoProducto.objects.select_related("producto", "almacen").order_by("-fecha")
    serializer_class = MovimientoProductoSerializer
