# apps/inventario/services/stock_service.py

from django.core.exceptions import ValidationError

from apps.inventario.models import StockProducto, MovimientoProducto



def validar_cantidad(cantidad):
    if cantidad <= 0:
        raise ValidationError("La cantidad debe ser mayor a 0.")


def validar_stock_suficiente(stock, cantidad):
    if stock.cantidad < cantidad:
        raise ValidationError("Stock insuficiente.")


def aumentar_stock(stock, cantidad):
    stock.cantidad += cantidad

from decimal import Decimal
import logging

from django.db import transaction

from apps.core.exceptions import CantidadInvalidaError, StockInsuficienteError
from apps.inventario.models import MovimientoProducto
from apps.inventario.services.inventario_service import obtener_stock_producto, registrar_movimiento

logger = logging.getLogger(__name__)


def validar_cantidad(cantidad):
    return _cantidad_decimal(cantidad)


def validar_stock_suficiente(stock, cantidad):
    cantidad = _cantidad_decimal(cantidad)
    if Decimal(stock.cantidad or 0) < cantidad:
        raise StockInsuficienteError("Stock insuficiente.")


def aumentar_stock(stock, cantidad):
    cantidad = _cantidad_decimal(cantidad)
    stock.cantidad = Decimal(stock.cantidad or 0) + cantidad
    return stock


def disminuir_stock(stock, cantidad):
    validar_stock_suficiente(stock, cantidad)
    stock.cantidad -= cantidad
    return stock




def salida_stock(producto, cantidad, tipo=None, usuario=None, observacion=""):
    if cantidad <= 0:
        raise ValidationError("La cantidad debe ser mayor a 0.")

    stock, _ = StockProducto.objects.get_or_create(
        producto=producto,
        defaults={"cantidad": 0}
    )

    if stock.cantidad < cantidad:
        raise ValidationError("Stock insuficiente.")

    stock.cantidad -= cantidad
    stock.save(update_fields=["cantidad"])

    MovimientoProducto.objects.create(
        producto=producto,
        cantidad=cantidad,
        tipo=tipo or MovimientoProducto.SALIDA,
        usuario=usuario,
        observacion=observacion
    )

    return stock

    cantidad = _cantidad_decimal(cantidad)
    validar_stock_suficiente(stock, cantidad)
    stock.cantidad = Decimal(stock.cantidad or 0) - cantidad
    return stock


def _cantidad_decimal(cantidad):
    cantidad = Decimal(str(cantidad))
    if cantidad <= 0:
        raise CantidadInvalidaError("La cantidad debe ser mayor a 0.")
    return cantidad


@transaction.atomic
def entrada_stock(item=None, cantidad=None, descripcion="", almacen=None, usuario=None, observacion=None, producto=None):
    item = item or producto
    if observacion is not None and not descripcion:
        descripcion = observacion
    cantidad = _cantidad_decimal(cantidad)
    stock = obtener_stock_producto(item, almacen)
    stock.cantidad = Decimal(stock.cantidad or 0) + cantidad
    stock.save(update_fields=["cantidad"])

    item.stock = stock.cantidad
    item.save(update_fields=["stock"])

    registrar_movimiento(
        producto=item,
        tipo=MovimientoProducto.ENTRADA,
        cantidad=cantidad,
        descripcion=descripcion,
        almacen=almacen,
    )
    logger.info("Entrada de stock | producto=%s | cantidad=%s", item.id, cantidad)
    return stock.cantidad


@transaction.atomic
def salida_stock(item=None, cantidad=None, descripcion="", almacen=None, tipo=MovimientoProducto.SALIDA, usuario=None, observacion=None, producto=None):
    item = item or producto
    if observacion is not None and not descripcion:
        descripcion = observacion
    cantidad = _cantidad_decimal(cantidad)
    stock = obtener_stock_producto(item, almacen)

    if Decimal(stock.cantidad or 0) < cantidad:
        raise StockInsuficienteError(f"Stock insuficiente para {item.nombre}.")

    stock.cantidad = Decimal(stock.cantidad or 0) - cantidad
    stock.save(update_fields=["cantidad"])

    item.stock = stock.cantidad
    item.save(update_fields=["stock"])

    registrar_movimiento(
        producto=item,
        tipo=tipo,
        cantidad=cantidad,
        descripcion=descripcion,
        almacen=almacen,
    )
    logger.info("Salida de stock | producto=%s | cantidad=%s | tipo=%s", item.id, cantidad, tipo)
    return stock.cantidad
