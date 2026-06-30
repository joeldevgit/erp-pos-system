from django.db import transaction

from apps.auditoria.services import registrar_auditoria
from apps.productos.dto import ProductoData
from apps.productos.repositories.producto_repository import ProductoRepository
from apps.productos.services.producto_service import activar_producto


class ActualizarProductoUseCase:

    @staticmethod
    @transaction.atomic
    def ejecutar(form, precios_formset=None, caducidades_formset=None, usuario=None):
        producto = form.save(commit=False)
        producto = activar_producto(producto)
        producto.save()
    """Actualiza productos desde DTO; mantiene compatibilidad con ``form``."""

    @staticmethod
    @transaction.atomic
    def ejecutar(producto=None, data: ProductoData | dict | None = None, precios_formset=None, caducidades_formset=None, usuario=None, form=None):
        if data is None and form is not None:
            data = ProductoData.from_form(form)
            producto = producto or form.instance
        elif isinstance(data, dict):
            data = ProductoData.from_dict(data)

        if producto is None:
            raise ValueError("Producto requerido para actualizar.")
        if data is None:
            raise ValueError("Datos de producto requeridos.")

        data.to_entity().validar()
        for campo, valor in data.to_model_dict().items():
            setattr(producto, campo, valor)

        producto = activar_producto(producto)
        ProductoRepository.guardar(producto)

        if precios_formset:
            precios_formset.instance = producto
            precios_formset.save()

        if caducidades_formset:
            caducidades_formset.instance = producto
            caducidades_formset.save()

        registrar_auditoria(
            usuario=usuario,
            accion="UPDATE",
            app="productos",
            modelo="Producto",
            objeto_id=producto.id,
            descripcion=f"Se actualizó el producto: {producto.nombre}"
        )

        return producto
        return producto
