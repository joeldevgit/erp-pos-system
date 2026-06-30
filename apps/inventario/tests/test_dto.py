from decimal import Decimal

from apps.inventario.dto import MermaData, MovimientoStockData


def test_merma_data_valida_datos_minimos():
    dto = MermaData(producto=object(), cantidad=Decimal("1"), motivo="Roto")
    dto.validar()


def test_movimiento_stock_data_valida_datos_minimos():
    dto = MovimientoStockData(producto=object(), cantidad=Decimal("1"), tipo="entrada")
    dto.validar()
