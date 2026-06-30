"""Contrato para repositorios de stock e inventario."""
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Any


class StockRepositoryPort(ABC):
    """Define operaciones mínimas para persistencia de stock."""

    @abstractmethod
    def obtener_o_crear(self, producto: Any, almacen: Any | None = None) -> Any:
        """Obtiene o crea el registro de stock del producto en un almacén."""
        raise NotImplementedError

    @abstractmethod
    def guardar(self, stock: Any) -> Any:
        """Persiste los cambios de cantidad del stock."""
        raise NotImplementedError

    @abstractmethod
    def registrar_movimiento(
        self,
        producto: Any,
        almacen: Any | None = None,
        cantidad: Decimal = Decimal("0"),
        tipo: str = "salida",
        usuario: Any | None = None,
        observacion: str = "",
        descripcion: str = "",
    ) -> Any:
        """Registra un movimiento de inventario."""
        raise NotImplementedError
