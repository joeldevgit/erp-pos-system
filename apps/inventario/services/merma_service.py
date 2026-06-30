import logging

from django.db import transaction

from apps.inventario.models import MermaProducto, MovimientoProducto
from apps.inventario.services.stock_service import salida_stock


logger = logging.getLogger(__name__)


@transaction.atomic
def registrar_merma(producto, cantidad, motivo, almacen=None):
    salida_stock(
        item=producto,
        cantidad=cantidad,
        descripcion=f"Merma: {motivo}",
        almacen=almacen,
        tipo=MovimientoProducto.MERMA
    )

    merma = MermaProducto.objects.create(
        producto=producto,
        cantidad=cantidad,
        motivo=motivo
    )

    logger.info(
        f"Merma registrada | producto={producto.id} | cantidad={cantidad}"
    )

    return merma