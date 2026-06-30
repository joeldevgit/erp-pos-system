from rest_framework import serializers

from apps.productos.models import Categoria, Producto, Unidad
from apps.inventario.models import Almacen, StockProducto, MovimientoProducto
from apps.productos.usecases.api_producto_usecase import ProductoAPIUseCase


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nombre", "estado"]


class UnidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidad
        fields = ["id", "nombre", "abreviatura"]


class ProductoSerializer(serializers.ModelSerializer):
    categoria_nombre = serializers.CharField(source="categoria.nombre", read_only=True)
    unidad_nombre = serializers.CharField(source="unidad.nombre", read_only=True)

    class Meta:
        model = Producto
        fields = [
            "id", "nombre", "codigo", "categoria", "categoria_nombre", "unidad", "unidad_nombre",
            "precio_compra", "precio_venta", "stock", "stock_minimo", "informacion_adicional", "estado",
        ]

    def create(self, validated_data):
        request = self.context.get("request")
        usuario = getattr(request, "user", None)
        return ProductoAPIUseCase.crear(validated_data, usuario=usuario)

    def update(self, instance, validated_data):
        request = self.context.get("request")
        usuario = getattr(request, "user", None)
        return ProductoAPIUseCase.actualizar(instance, validated_data, usuario=usuario)


class AlmacenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Almacen
        fields = ["id", "nombre", "estado"]


class StockProductoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source="producto.nombre", read_only=True)
    almacen_nombre = serializers.CharField(source="almacen.nombre", read_only=True)

    class Meta:
        model = StockProducto
        fields = ["id", "producto", "producto_nombre", "almacen", "almacen_nombre", "cantidad"]


class MovimientoProductoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source="producto.nombre", read_only=True)
    almacen_nombre = serializers.CharField(source="almacen.nombre", read_only=True)

    class Meta:
        model = MovimientoProducto
        fields = ["id", "producto", "producto_nombre", "almacen", "almacen_nombre", "tipo", "cantidad", "descripcion", "fecha"]
