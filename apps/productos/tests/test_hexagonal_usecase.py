from decimal import Decimal

from apps.productos.application.use_cases import CrearProductoHexagonalUseCase
from apps.productos.domain.entities import ProductoEntity
from apps.productos.infrastructure.django_repositories import DjangoProductoRepository


def test_crear_producto_hexagonal_usecase(db):
    usecase = CrearProductoHexagonalUseCase(DjangoProductoRepository())
    producto = usecase.ejecutar(
        ProductoEntity(
            nombre="Producto Hexagonal",
            precio_compra=Decimal("10.00"),
            precio_venta=Decimal("15.00"),
            codigo="HEX-001",
            stock=Decimal("5.00"),
        )
    )
    assert producto.id
    assert producto.nombre == "Producto Hexagonal"
