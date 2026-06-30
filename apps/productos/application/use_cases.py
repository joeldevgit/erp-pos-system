from django.db import transaction

from apps.auditoria.services import registrar_auditoria
from apps.core.events import DomainEvent, publicar_evento
from apps.productos.domain.entities import ProductoEntity
from apps.productos.domain.repositories import ProductoRepositoryPort


class CrearProductoHexagonalUseCase:
    """Caso de uso puro de aplicación: no conoce Views ni Serializers."""

    def __init__(self, repository: ProductoRepositoryPort):
        self.repository = repository

    @transaction.atomic
    def ejecutar(self, entity: ProductoEntity, *, usuario=None, request=None):
        entity.validar()
        producto = self.repository.crear_desde_entidad(entity)
        registrar_auditoria(
            usuario=usuario,
            accion="CREATE",
            app="productos",
            modelo="Producto",
            objeto_id=producto.id,
            descripcion=f"Se creó el producto desde use case hexagonal: {producto.nombre}",
            request=request,
        )
        publicar_evento(DomainEvent(nombre="producto.creado", data={"producto_id": producto.id}))
        return producto
