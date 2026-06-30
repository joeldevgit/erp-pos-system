from django.db import transaction

from apps.auditoria.services import registrar_auditoria
from apps.core.events import DomainEvent, publicar_evento
from apps.productos.models import Producto
from apps.productos.repositories.producto_repository import ProductoRepository
from apps.productos.services.producto_service import activar_producto, cambiar_estado


class ProductoAPIUseCase:
    """Casos de uso para que la API no escriba directo contra el ORM."""

    @staticmethod
    @transaction.atomic
    def crear(data, usuario=None):
        producto = Producto(**data)
        producto = activar_producto(producto)
        producto.save()

        registrar_auditoria(
            usuario=usuario,
            accion="CREATE",
            app="productos",
            modelo="Producto",
            objeto_id=producto.id,
            descripcion=f"API creó el producto: {producto.nombre}",
        )
        publicar_evento(DomainEvent(nombre="producto.creado", data={"producto_id": producto.id}))
        return producto

    @staticmethod
    @transaction.atomic
    def actualizar(producto, data, usuario=None):
        for campo, valor in data.items():
            setattr(producto, campo, valor)
        ProductoRepository.guardar(producto)

        registrar_auditoria(
            usuario=usuario,
            accion="UPDATE",
            app="productos",
            modelo="Producto",
            objeto_id=producto.id,
            descripcion=f"API actualizó el producto: {producto.nombre}",
        )
        publicar_evento(DomainEvent(nombre="producto.actualizado", data={"producto_id": producto.id}))
        return producto

    @staticmethod
    @transaction.atomic
    def cambiar_estado(producto, usuario=None):
        producto = cambiar_estado(producto)
        ProductoRepository.guardar(producto, update_fields=["estado"])
        registrar_auditoria(
            usuario=usuario,
            accion="UPDATE",
            app="productos",
            modelo="Producto",
            objeto_id=producto.id,
            descripcion=f"API cambió estado del producto: {producto.nombre}",
        )
        return producto
