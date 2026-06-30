from apps.inventario.models import MermaProducto
from apps.inventario.models import Almacen, MermaProducto, MovimientoProducto, StockProducto


class AlmacenRepository:
    @staticmethod
    def principal():
        almacen, _ = Almacen.objects.get_or_create(nombre="PRINCIPAL", defaults={"estado": True})
        return almacen


class StockRepository:
    @staticmethod
    def obtener_o_crear(producto, almacen=None):
        almacen = almacen or AlmacenRepository.principal()
        stock, _ = StockProducto.objects.get_or_create(
            producto=producto,
            almacen=almacen,
            defaults={"cantidad": producto.stock or 0},
        )
        return stock

    @staticmethod
    def guardar(stock):
        stock.save(update_fields=["cantidad"])
        stock.producto.stock = stock.cantidad
        stock.producto.save(update_fields=["stock"])
        return stock


class MovimientoRepository:
    @staticmethod
    def crear(producto, almacen=None, cantidad=0, tipo=MovimientoProducto.SALIDA, usuario=None, observacion="", descripcion=""):
        almacen = almacen or AlmacenRepository.principal()
        return MovimientoProducto.objects.create(
            producto=producto,
            almacen=almacen,
            cantidad=cantidad,
            tipo=tipo,
            descripcion=descripcion or observacion,
        )


class MermaRepository:
    @staticmethod
    def listar():
        return MermaProducto.objects.select_related("producto").order_by("-fecha")

    @staticmethod
    def crear(**data):
        return MermaProducto.objects.create(**data)
        return MermaProducto.objects.create(**data)
