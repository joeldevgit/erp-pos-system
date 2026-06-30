from decimal import Decimal

import pytest

from apps.inventario.application.use_cases import RegistrarMovimientoStockUseCase
from apps.inventario.domain.entities import MovimientoStockEntity
from apps.inventario.infrastructure.django_repositories import DjangoStockRepository
from apps.inventario.models import MovimientoProducto
from apps.productos.models import Categoria, Producto, Unidad


class FakeStockRepository:
    def __init__(self):
        self.entity = None
        self.almacen = None

    def registrar_movimiento(self, entity, *, almacen=None):
        self.entity = entity
        self.almacen = almacen
        return {"ok": True, "tipo": entity.tipo}


def test_movimiento_stock_entity_valida_cantidad():
    MovimientoStockEntity(producto_id=1, cantidad=Decimal("1"), tipo=MovimientoProducto.ENTRADA).validar()
    with pytest.raises(ValueError):
        MovimientoStockEntity(producto_id=1, cantidad=Decimal("0"), tipo=MovimientoProducto.ENTRADA).validar()


@pytest.mark.django_db
def test_registrar_movimiento_stock_usecase_usa_puerto_repository():
    repo = FakeStockRepository()
    usecase = RegistrarMovimientoStockUseCase(repo)
    entity = MovimientoStockEntity(producto_id=1, cantidad=Decimal("3"), tipo=MovimientoProducto.SALIDA)

    result = usecase.ejecutar(entity, almacen="A1")

    assert result == {"ok": True, "tipo": MovimientoProducto.SALIDA}
    assert repo.entity == entity
    assert repo.almacen == "A1"


@pytest.mark.django_db
def test_django_stock_repository_registra_movimiento_real():
    categoria = Categoria.objects.create(nombre="Cat")
    unidad = Unidad.objects.create(nombre="Unidad", abreviatura="UND")
    producto = Producto.objects.create(
        nombre="Producto Stock",
        codigo="STK-001",
        categoria=categoria,
        unidad=unidad,
        precio_compra=Decimal("1.00"),
        precio_venta=Decimal("2.00"),
    )
    entity = MovimientoStockEntity(
        producto_id=producto.id,
        cantidad=Decimal("5"),
        tipo=MovimientoProducto.ENTRADA,
        descripcion="entrada hexagonal",
    )

    movimiento = DjangoStockRepository().registrar_movimiento(entity)

    assert movimiento.producto == producto
    assert movimiento.cantidad == Decimal("5")
    assert movimiento.tipo == MovimientoProducto.ENTRADA
