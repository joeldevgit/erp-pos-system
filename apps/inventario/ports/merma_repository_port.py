"""Contrato para persistencia de mermas."""
from abc import ABC, abstractmethod
from typing import Any


class MermaRepositoryPort(ABC):
    """Define operaciones mínimas para mermas de inventario."""

    @abstractmethod
    def listar(self):
        """Lista las mermas registradas."""
        raise NotImplementedError

    @abstractmethod
    def crear(self, **data: Any) -> Any:
        """Crea una merma con los datos validados."""
        raise NotImplementedError
