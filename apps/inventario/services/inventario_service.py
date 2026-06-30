from django.db import transaction

from apps.inventario.models import Almacen, StockProducto, MovimientoProducto


def obtener_almacen_principal():
    almacen, _ = Almacen.objects.get_or_create(
        nombre="PRINCIPAL",
        defaults={"estado": True}
    )
    return almacen



def obtener_stock_producto(producto, almacen=None):
    if almacen is None:
        almacen = obtener_almacen_principal()

    # Inicializar la cantidad del stock por almacén usando el stock del producto
    defaults = {"cantidad": producto.stock or 0}

    stock, _ = StockProducto.objects.get_or_create(
        producto=producto,
        almacen=almacen,
        defaults=defaults
    )

    return stock


@transaction.atomic
def registrar_movimiento(producto, tipo, cantidad, descripcion="", almacen=None):
    if almacen is None:
        almacen = obtener_almacen_principal()

    return MovimientoProducto.objects.create(
        producto=producto,
        almacen=almacen,
        tipo=tipo,
        cantidad=cantidad,
        descripcion=descripcion
    )