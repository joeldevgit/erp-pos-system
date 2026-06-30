from django.db import transaction

from apps.inventario.domain.entities import MovimientoStockEntity
from apps.inventario.domain.repositories import StockRepositoryPort


class RegistrarMovimientoStockUseCase:
    def __init__(self, repository: StockRepositoryPort):
        self.repository = repository

    @transaction.atomic
    def ejecutar(self, entity: MovimientoStockEntity, *, almacen=None):
        entity.validar()
        return self.repository.registrar_movimiento(entity, almacen=almacen)
