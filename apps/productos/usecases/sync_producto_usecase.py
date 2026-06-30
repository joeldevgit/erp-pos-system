from django.db import transaction

from apps.auditoria.services import registrar_auditoria
from apps.productos.repositories.producto_repository import ProductoRepository
from apps.productos.services.producto_service import (
    obtener_o_crear_categoria,
    obtener_o_crear_unidad,
)


class SyncProductoUseCase:

    @staticmethod
    @transaction.atomic
    def ejecutar(data, usuario=None):
        nombre = data.get("nombre")
        precio_compra = data.get("precio_compra")
        precio_venta = data.get("precio_venta")
        codigo = data.get("codigo")

        producto = ProductoRepository.buscar_por_codigo(codigo)

        if not producto:
            producto = ProductoRepository.buscar_por_datos(
                nombre=nombre,
                precio_compra=precio_compra,
                precio_venta=precio_venta
            )

        if producto:
            return producto, "exists"

        categoria = obtener_o_crear_categoria(data.get("categoria"))
        unidad = obtener_o_crear_unidad(data.get("unidad"))

        producto = ProductoRepository.crear(
            nombre=nombre,
            precio_compra=precio_compra,
            precio_venta=precio_venta,
            codigo=codigo or None,
            categoria=categoria,
            unidad=unidad,
            stock=data.get("stock") or 0,
            stock_minimo=data.get("stock_minimo") or 0,
            informacion_adicional=data.get("informacion_adicional", ""),
            estado=True,
        )

        registrar_auditoria(
            usuario=usuario,
            accion="CREATE",
            app="productos",
            modelo="Producto",
            objeto_id=producto.id,
            descripcion=f"Se creó producto por sincronización: {producto.nombre}"
        )

        return producto, "created"