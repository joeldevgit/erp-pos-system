from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.inventario.models import MovimientoProducto
from apps.inventario.services.inventario_service import (
    obtener_stock_producto,
    registrar_movimiento,
)

from apps.core.exceptions import (
    StockInsuficienteError,
    CantidadInvalidaError,
)

import logging

logger = logging.getLogger(__name__)



@transaction.atomic
def entrada_stock(item, cantidad, descripcion="", almacen=None):
    cantidad = Decimal(cantidad)

    if cantidad <= 0:
        raise CantidadInvalidaError(
            "La cantidad debe ser mayor a 0."
        )

    stock = obtener_stock_producto(item, almacen)
    stock.cantidad += cantidad
    stock.save(update_fields=["cantidad"])

    item.stock = stock.cantidad
    item.save(update_fields=["stock"])

    

    registrar_movimiento(
        producto=item,
        tipo=MovimientoProducto.ENTRADA,
        cantidad=cantidad,
        descripcion=descripcion,
        almacen=almacen
    )

    return stock.cantidad


@transaction.atomic
def salida_stock(item, cantidad, descripcion="", almacen=None, tipo=MovimientoProducto.SALIDA):
    cantidad = Decimal(cantidad)

    if cantidad <= 0:
        raise CantidadInvalidaError(
            "La cantidad debe ser mayor a 0."
        )

    stock = obtener_stock_producto(item, almacen)

    if Decimal(stock.cantidad or 0) < cantidad:
        raise StockInsuficienteError(
            f"Stock insuficiente para {item.nombre}."
        )

    nuevo_stock = Decimal(stock.cantidad or 0) - cantidad

    stock.cantidad = nuevo_stock
    stock.save(update_fields=["cantidad"])

    item.stock = nuevo_stock
    item.save(update_fields=["stock"])

    registrar_movimiento(
        producto=item,
        tipo=tipo,
        cantidad=cantidad,
        descripcion=descripcion,
        almacen=almacen
    )

    return stock.cantidad