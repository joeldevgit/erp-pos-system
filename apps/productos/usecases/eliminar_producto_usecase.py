from django.db import transaction

from apps.auditoria.services import registrar_auditoria
from apps.productos.repositories.producto_repository import ProductoRepository


class EliminarProductoUseCase:

    @staticmethod
    @transaction.atomic
    def ejecutar(producto, usuario=None):
        producto_id = producto.id
        nombre = producto.nombre

        ProductoRepository.eliminar(producto)

        registrar_auditoria(
            usuario=usuario,
            accion="DELETE",
            app="productos",
            modelo="Producto",
            objeto_id=producto_id,
            descripcion=f"Se eliminó el producto: {nombre}"
        )