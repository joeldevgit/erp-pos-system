from decimal import Decimal

import pytest

from apps.productos.domain.entities import ProductoEntity
from apps.productos.models import Categoria, Producto, Unidad
from apps.productos.repositories.producto_repository import ProductoRepository
from apps.productos.services.producto_service import (
    activar_producto,
    obtener_o_crear_categoria,
    obtener_o_crear_unidad,
)


@pytest.mark.django_db
def test_producto_entity_valida_datos_correctos_y_errores():
    ProductoEntity(nombre="Producto", precio_compra=Decimal("1"), precio_venta=Decimal("2"), stock=Decimal("0")).validar()

    for entity in [
        ProductoEntity(nombre=" ", precio_compra=Decimal("1"), precio_venta=Decimal("2")),
        ProductoEntity(nombre="X", precio_compra=Decimal("-1"), precio_venta=Decimal("2")),
        ProductoEntity(nombre="X", precio_compra=Decimal("1"), precio_venta=Decimal("-2")),
        ProductoEntity(nombre="X", precio_compra=Decimal("1"), precio_venta=Decimal("2"), stock=Decimal("-1")),
    ]:
        with pytest.raises(ValueError):
            entity.validar()


@pytest.mark.django_db
def test_producto_repository_busquedas_guardado_y_eliminacion():
    categoria = Categoria.objects.create(nombre="Cat")
    unidad = Unidad.objects.create(nombre="Unidad", abreviatura="UND")
    producto = ProductoRepository.crear(
        nombre="Repo Producto",
        codigo="REP-001",
        categoria=categoria,
        unidad=unidad,
        precio_compra=Decimal("10.00"),
        precio_venta=Decimal("15.00"),
    )

    assert ProductoRepository.obtener_por_id(producto.id) == producto
    assert ProductoRepository.buscar_por_codigo(None) is None
    assert ProductoRepository.buscar_por_codigo("REP-001") == producto
    assert ProductoRepository.buscar_por_datos("Repo Producto", Decimal("10.00"), Decimal("15.00")) == producto
    assert list(ProductoRepository.listar_todos()) == [producto]

    producto.nombre = "Repo Producto Editado"
    ProductoRepository.guardar(producto, update_fields=["nombre"])
    producto.refresh_from_db()
    assert producto.nombre == "Repo Producto Editado"

    ProductoRepository.eliminar(producto)
    assert not Producto.objects.filter(id=producto.id).exists()


@pytest.mark.django_db
def test_producto_service_activa_y_crea_catalogos_normalizados():
    categoria = obtener_o_crear_categoria("  tecnología  ")
    unidad = obtener_o_crear_unidad("  unidad  ")

    assert categoria.nombre == "Tecnología"
    assert unidad.nombre == "Unidad"
    assert obtener_o_crear_categoria(" ") is None
    assert obtener_o_crear_unidad(" ") is None

    producto = Producto(nombre="X", estado=False, precio_compra=Decimal("1"), precio_venta=Decimal("2"))
    assert activar_producto(producto).estado is True
