from decimal import Decimal
from django.test import TestCase

from apps.productos.models import Producto
from apps.inventario.services.stock_service import (
    entrada_stock,
    salida_stock,
)

from apps.core.exceptions import (
    StockInsuficienteError,
    CantidadInvalidaError,
)


class StockServiceTest(TestCase):

    def test_descuenta_stock(self):
        producto = Producto.objects.create(
            nombre="Laptop",
            precio_compra=Decimal("1000.00"),
            precio_venta=Decimal("1200.00"),
            stock=Decimal("0.00"),
            estado=True
        )

        entrada_stock(producto, Decimal("10"))

        stock_final = salida_stock(producto, Decimal("3"))

        self.assertEqual(stock_final, Decimal("7"))

    def test_no_permite_stock_negativo(self):
        producto = Producto.objects.create(
            nombre="Monitor",
            precio_compra=Decimal("500.00"),
            precio_venta=Decimal("700.00"),
            stock=Decimal("0.00"),
            estado=True
        )

        entrada_stock(producto, Decimal("5"))

        with self.assertRaises(StockInsuficienteError):
            salida_stock(producto, Decimal("10"))

    def test_no_permite_cantidad_cero(self):
        producto = Producto.objects.create(
            nombre="Teclado",
            precio_compra=Decimal("50.00"),
            precio_venta=Decimal("80.00"),
            stock=Decimal("0.00"),
            estado=True
        )

        with self.assertRaises(CantidadInvalidaError):
            entrada_stock(producto, Decimal("0"))

    def test_no_permite_cantidad_negativa(self):
        producto = Producto.objects.create(
            nombre="Mouse",
            precio_compra=Decimal("20.00"),
            precio_venta=Decimal("35.00"),
            stock=Decimal("0.00"),
            estado=True
        )

        with self.assertRaises(CantidadInvalidaError):
            entrada_stock(producto, Decimal("-5"))
            entrada_stock(producto, Decimal("-5"))
import pytest
from apps.core.exceptions import CantidadInvalidaError, StockInsuficienteError
from apps.inventario.services.stock_service import validar_cantidad, validar_stock_suficiente, aumentar_stock, disminuir_stock
from apps.inventario.services.inventario_service import obtener_stock_producto


def test_validar_cantidad_invalida():
    with pytest.raises(CantidadInvalidaError):
        validar_cantidad(0)


@pytest.mark.django_db
def test_helpers_stock():
    producto = Producto.objects.create(nombre="Helper", precio_compra=Decimal("1.00"), precio_venta=Decimal("2.00"), stock=Decimal("10.00"), estado=True)
    stock = obtener_stock_producto(producto)
    aumentar_stock(stock, 5)
    assert stock.cantidad == 15
    disminuir_stock(stock, 3)
    assert stock.cantidad == 12
    validar_stock_suficiente(stock, 12)
    with pytest.raises(StockInsuficienteError):
        validar_stock_suficiente(stock, 13)
