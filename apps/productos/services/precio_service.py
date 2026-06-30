from apps.productos.models import PrecioAdicional


def listar_precios_producto(producto):
    return producto.precios_adicionales.all()


def crear_precio_adicional(producto, nombre, precio):
    return PrecioAdicional.objects.create(
        producto=producto,
        nombre=nombre,
        precio=precio
    )


def eliminar_precios_producto(producto):
    return PrecioAdicional.objects.filter(producto=producto).delete()