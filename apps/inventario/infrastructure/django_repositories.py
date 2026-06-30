from django.shortcuts import get_object_or_404

from apps.inventario.domain.entities import MovimientoStockEntity
from apps.inventario.models import MovimientoProducto
from apps.inventario.repositories.inventario_repository import MovimientoRepository
from apps.productos.models import Producto


class DjangoStockRepository:
    def registrar_movimiento(self, entity: MovimientoStockEntity, *, almacen=None):
        producto = get_object_or_404(Producto, id=entity.producto_id)
        return MovimientoRepository.crear(
            producto=producto,
            almacen=almacen,
            cantidad=entity.cantidad,
            tipo=entity.tipo or MovimientoProducto.SALIDA,
            descripcion=entity.descripcion,
        )
