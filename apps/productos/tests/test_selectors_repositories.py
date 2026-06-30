import pytest

from apps.productos.models import Categoria, Producto, Unidad
from apps.productos.repositories.producto_repository import CategoriaRepository, ProductoRepository, UnidadRepository
from apps.productos.selectors import (
    buscar_productos,
    buscar_productos_activos,
    listar_categorias,
    listar_productos,
    listar_productos_activos,
    listar_unidades,
    obtener_producto_por_id,
    productos_stock_bajo,
)


@pytest.mark.django_db
def test_selectors_y_repositories_producto():
    categoria = CategoriaRepository.obtener_o_crear("Categoria A")
    unidad = UnidadRepository.obtener_o_crear("Unidad A")
    producto = ProductoRepository.crear(
        nombre="Mouse",
        codigo="MOU-1",
        categoria=categoria,
        unidad=unidad,
        precio_compra=10,
        precio_venta=15,
        stock=0,
        stock_minimo=1,
        estado=True,
    )
    Producto.objects.create(nombre="Teclado", codigo="TEC-1", categoria=categoria, unidad=unidad, estado=False, stock=5, precio_compra=1, precio_venta=2)

    assert ProductoRepository.obtener_por_id(producto.id) == producto
    assert ProductoRepository.listar_todos().count() == 2
    producto.nombre = "Mouse Pro"
    ProductoRepository.guardar(producto)
    assert ProductoRepository.obtener_por_id(producto.id).nombre == "Mouse Pro"

    assert listar_productos().count() == 2
    assert listar_productos_activos().count() == 1
    assert buscar_productos("Mouse").count() == 1
    assert buscar_productos_activos("Mouse").count() == 1
    assert obtener_producto_por_id(producto.id) == producto
    assert productos_stock_bajo().count() == 1
    assert list(listar_categorias()) == [categoria]
    assert list(listar_unidades()) == [unidad]
