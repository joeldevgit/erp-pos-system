from django.db import transaction

from apps.inventario.dto import MermaData
from apps.inventario.models import MovimientoProducto
from apps.inventario.repositories.inventario_repository import MermaRepository
from apps.inventario.services.stock_service import salida_stock


class RegistrarMermaUseCase:

    @staticmethod
    @transaction.atomic
    def ejecutar(producto, cantidad, motivo, usuario=None):
        salida_stock(
            producto=producto,
            cantidad=cantidad,
            tipo="MERMA",
            usuario=usuario,
            observacion=motivo
        )

        merma = MermaRepository.crear(
            producto=producto,
            cantidad=cantidad,
            motivo=motivo
        )

        return merma
    """Registra merma usando DTO de aplicación y movimiento de stock atómico."""

    @staticmethod
    @transaction.atomic
    def ejecutar(data: MermaData | None = None, producto=None, cantidad=None, motivo="", usuario=None):
        if data is None:
            data = MermaData(producto=producto, cantidad=cantidad, motivo=motivo, usuario=usuario)

        data.validar()
        usuario = usuario or data.usuario

        salida_stock(
            producto=data.producto,
            cantidad=data.cantidad,
            tipo=MovimientoProducto.MERMA,
            usuario=usuario,
            observacion=data.motivo
        )

        return MermaRepository.crear(
            producto=data.producto,
            cantidad=data.cantidad,
            motivo=data.motivo
        )
