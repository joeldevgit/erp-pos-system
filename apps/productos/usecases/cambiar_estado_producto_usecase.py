from django.db import transaction

from apps.auditoria.services import registrar_auditoria
from apps.productos.repositories.producto_repository import ProductoRepository
from apps.productos.services.producto_service import cambiar_estado


class CambiarEstadoProductoUseCase:

    @staticmethod
    @transaction.atomic
    def ejecutar(producto, usuario=None):
        producto = cambiar_estado(producto)

        ProductoRepository.guardar(
            producto,
            update_fields=["estado"]
        )

        registrar_auditoria(
            usuario=usuario,
            accion="UPDATE",
            app="productos",
            modelo="Producto",
            objeto_id=producto.id,
            descripcion=f"Se cambió el estado del producto: {producto.nombre}"
        )

        return producto