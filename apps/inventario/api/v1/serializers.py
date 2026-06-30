from rest_framework import serializers

from apps.inventario.models import Almacen, MermaProducto, MovimientoProducto, StockProducto


class AlmacenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Almacen
        fields = "__all__"


class StockProductoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source="producto.nombre", read_only=True)
    almacen_nombre = serializers.CharField(source="almacen.nombre", read_only=True)

    class Meta:
        model = StockProducto
        fields = "__all__"


class MovimientoProductoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source="producto.nombre", read_only=True)
    almacen_nombre = serializers.CharField(source="almacen.nombre", read_only=True)

    class Meta:
        model = MovimientoProducto
        fields = "__all__"
        read_only_fields = ("fecha",)


class MermaProductoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source="producto.nombre", read_only=True)

    class Meta:
        model = MermaProducto
        fields = "__all__"
        read_only_fields = ("fecha",)
