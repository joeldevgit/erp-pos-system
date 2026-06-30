from apps.productos.models import Producto, Categoria, Unidad


def listar_productos():
    return (
        Producto.objects
        .select_related("categoria", "unidad")
        .order_by("-id")
    )


def listar_productos_activos():
    return listar_productos().filter(estado=True)


def buscar_productos(q=None):
    productos = listar_productos_activos()

    if q:
        productos = productos.filter(nombre__icontains=q)

    return productos


def obtener_producto_por_id(producto_id):
    return (
        Producto.objects
        .select_related("categoria", "unidad")
        .filter(id=producto_id)
        .first()
    )


def listar_categorias():
    return Categoria.objects.all().order_by("nombre")


def listar_unidades():
    return Unidad.objects.all().order_by("nombre")


def productos_stock_bajo():
    return (
        Producto.objects
        .filter(estado=True, stock__lte=0)
        .select_related("categoria", "unidad")
        .order_by("stock", "nombre")
    )


def buscar_productos_activos(q=None):
    productos = listar_productos_activos()

    if q:
        productos = productos.filter(nombre__icontains=q)

    return productos