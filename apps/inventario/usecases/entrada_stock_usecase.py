# apps/inventario/usecases/entrada_stock_usecase.py

from django.db import transaction

from apps.inventario.repositories.inventario_repository import (
    StockRepository,
    MovimientoRepository,
)
from apps.inventario.services.stock_service import validar_cantidad, aumentar_stock
from apps.inventario.models import MovimientoProducto


class EntradaStockUseCase:

    @staticmethod
    @transaction.atomic
    def ejecutar(producto, cantidad, almacen=None, usuario=None, observacion=""):
        validar_cantidad(cantidad)

        stock = StockRepository.obtener_o_crear(
            producto=producto,
            almacen=almacen
        )


from django.db import transaction

from apps.inventario.dto import MovimientoStockData
from apps.inventario.models import MovimientoProducto
from apps.inventario.repositories.inventario_repository import MovimientoRepository, StockRepository
from apps.inventario.services.stock_service import aumentar_stock, validar_cantidad


class EntradaStockUseCase:
    @staticmethod
    @transaction.atomic
    def ejecutar(data: MovimientoStockData | None = None, producto=None, cantidad=None, almacen=None, usuario=None, observacion=""):
        if data is None:
            data = MovimientoStockData(
                producto=producto,
                cantidad=cantidad,
                tipo=MovimientoProducto.ENTRADA,
                almacen=almacen,
                usuario=usuario,
                observacion=observacion,
            )
        data.validar()
        cantidad = validar_cantidad(data.cantidad)

        stock = StockRepository.obtener_o_crear(producto=data.producto, almacen=data.almacen)
        stock = aumentar_stock(stock, cantidad)
        StockRepository.guardar(stock)

        MovimientoRepository.crear(
            producto=producto,
            almacen=almacen,
            cantidad=cantidad,
            tipo=MovimientoProducto.ENTRADA,
            usuario=usuario,
            observacion=observacion
        )

        return stock

            producto=data.producto,
            almacen=data.almacen,
            cantidad=cantidad,
            tipo=MovimientoProducto.ENTRADA,
            usuario=data.usuario,
            observacion=data.observacion,
        )
        return stock
