# apps/inventario/usecases/salida_stock_usecase.py

from django.db import transaction

from apps.inventario.repositories.inventario_repository import (
    StockRepository,
    MovimientoRepository,
)
from apps.inventario.services.stock_service import validar_cantidad, disminuir_stock
from apps.inventario.models import MovimientoProducto


class SalidaStockUseCase:

    @staticmethod
    @transaction.atomic
    def ejecutar(producto, cantidad, almacen=None, usuario=None, observacion="", tipo=None):
        validar_cantidad(cantidad)

        stock = StockRepository.obtener_o_crear(
            producto=producto,
            almacen=almacen
        )


from django.db import transaction

from apps.inventario.dto import MovimientoStockData
from apps.inventario.models import MovimientoProducto
from apps.inventario.repositories.inventario_repository import MovimientoRepository, StockRepository
from apps.inventario.services.stock_service import disminuir_stock, validar_cantidad


class SalidaStockUseCase:
    @staticmethod
    @transaction.atomic
    def ejecutar(data: MovimientoStockData | None = None, producto=None, cantidad=None, almacen=None, usuario=None, observacion="", tipo=None):
        if data is None:
            data = MovimientoStockData(
                producto=producto,
                cantidad=cantidad,
                tipo=tipo or MovimientoProducto.SALIDA,
                almacen=almacen,
                usuario=usuario,
                observacion=observacion,
            )
        data.validar()
        cantidad = validar_cantidad(data.cantidad)

        stock = StockRepository.obtener_o_crear(producto=data.producto, almacen=data.almacen)
        stock = disminuir_stock(stock, cantidad)
        StockRepository.guardar(stock)

        MovimientoRepository.crear(
            producto=producto,
            almacen=almacen,
            cantidad=cantidad,
            tipo=tipo or MovimientoProducto.SALIDA,
            usuario=usuario,
            observacion=observacion
        )

        return stock

            producto=data.producto,
            almacen=data.almacen,
            cantidad=cantidad,
            tipo=data.tipo or MovimientoProducto.SALIDA,
            usuario=data.usuario,
            observacion=data.observacion,
        )
        return stock
