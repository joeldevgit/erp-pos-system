import pytest

from apps.inventario.models import MovimientoProducto
from apps.inventario.repositories.inventario_repository import AlmacenRepository, MermaRepository, MovimientoRepository, StockRepository
from apps.inventario.services.merma_service import registrar_merma
from apps.productos.models import Categoria, Producto, Unidad


@pytest.fixture
def producto():
    categoria = Categoria.objects.create(nombre="Cat")
    unidad = Unidad.objects.create(nombre="Und")
    return Producto.objects.create(nombre="Producto", categoria=categoria, unidad=unidad, stock=10, precio_compra=1, precio_venta=2)


@pytest.mark.django_db
def test_repositories_stock_movimiento_y_merma(producto):
    almacen = AlmacenRepository.principal()
    stock = StockRepository.obtener_o_crear(producto, almacen)
    stock.cantidad = 7
    StockRepository.guardar(stock)

    movimiento = MovimientoRepository.crear(producto=producto, almacen=almacen, cantidad=1, tipo=MovimientoProducto.SALIDA)
    merma = MermaRepository.crear(producto=producto, cantidad=1, motivo="Roto")

    assert almacen.nombre == "PRINCIPAL"
    assert producto.stock == 7
    assert movimiento.tipo == MovimientoProducto.SALIDA
    assert MermaRepository.listar().first() == merma


@pytest.mark.django_db
def test_registrar_merma_descuenta_stock(producto):
    merma = registrar_merma(producto=producto, cantidad=2, motivo="Vencido")
    producto.refresh_from_db()

    assert merma.cantidad == 2
    assert producto.stock == 8

from apps.inventario.selectors import listar_mermas


@pytest.mark.django_db
def test_selector_listar_mermas(producto):
    MermaRepository.crear(producto=producto, cantidad=1, motivo="Prueba")
    assert listar_mermas().count() == 1
