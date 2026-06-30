from decimal import Decimal

from apps.productos.dto import ProductoData


def test_producto_data_convierte_a_entidad_valida():
    dto = ProductoData(nombre="Laptop", precio_compra=Decimal("10"), precio_venta=Decimal("15"))
    entity = dto.to_entity()
    entity.validar()
    assert entity.nombre == "Laptop"
