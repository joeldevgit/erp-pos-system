from apps.productos.models import CaducidadProducto


def listar_caducidades_producto(producto):
    return producto.caducidades.all().order_by("fecha_caducidad")


def crear_caducidad(producto, lote, fecha_caducidad, informacion=""):
    return CaducidadProducto.objects.create(
        producto=producto,
        lote=lote,
        fecha_caducidad=fecha_caducidad,
        informacion=informacion
    )


def eliminar_caducidades_producto(producto):
    return CaducidadProducto.objects.filter(producto=producto).delete()