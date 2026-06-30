from typing import Protocol

from .entities import MovimientoStockEntity


class StockRepositoryPort(Protocol):
    def registrar_movimiento(self, entity: MovimientoStockEntity, *, almacen=None): ...
