from django.db import transaction

from apps.auditoria.services import registrar_auditoria
from apps.core.events import DomainEvent, publicar_evento
from apps.productos.dto import ProductoData
from apps.productos.models import Producto
from apps.productos.services.producto_service import activar_producto


class CrearProductoUseCase:
    """
    Crea productos sin depender de Django Forms.

    Compatibilidad: acepta DTO, dict o form.
    """

    @staticmethod
    @transaction.atomic
    def ejecutar(
        data: ProductoData | dict | None = None,
        precios_formset=None,
        caducidades_formset=None,
        usuario=None,
        form=None,
    ):
        if data is None and form is not None:
            data = ProductoData.from_form(form)
        elif isinstance(data, dict):
            data = ProductoData.from_dict(data)

        if data is None:
            raise ValueError("Datos de producto requeridos.")

        data.to_entity().validar()

        producto = Producto(**data.to_model_dict())
        producto = activar_producto(producto)
        producto.save()

        if precios_formset:
            precios_formset.instance = producto
            precios_formset.save()

        if caducidades_formset:
            caducidades_formset.instance = producto
            caducidades_formset.save()

        registrar_auditoria(
            usuario=usuario,
            accion="CREATE",
            app="productos",
            modelo="Producto",
            objeto_id=producto.id,
            descripcion=f"Se creó el producto: {producto.nombre}",
        )

        publicar_evento(
            DomainEvent(
                nombre="producto.creado",
                data={
                    "producto_id": producto.id,
                    "nombre": producto.nombre,
                },
            )
        )

        return producto