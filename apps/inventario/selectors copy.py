from apps.inventario.models import MermaProducto, MovimientoProducto, StockProducto, Almacen


def listar_mermas():
    return (
        MermaProducto.objects
        .select_related("producto")
        .order_by("-fecha")
    )


def listar_movimientos():
    return (
        MovimientoProducto.objects
        .select_related("producto", "almacen")
        .order_by("-fecha")
    )


def listar_stock_por_almacen():
    return (
        StockProducto.objects
        .select_related("producto", "almacen")
        .order_by("producto__nombre")
    )


def obtener_stock_producto(producto, almacen=None):
    qs = StockProducto.objects.select_related("producto", "almacen").filter(
        producto=producto
    )

    if almacen:
        qs = qs.filter(almacen=almacen)

    return qs.first()


def listar_almacenes_activos():
    return Almacen.objects.filter(estado=True).order_by("nombre")