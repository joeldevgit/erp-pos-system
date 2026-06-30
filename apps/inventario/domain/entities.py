from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class MovimientoStockEntity:
    producto_id: int
    cantidad: Decimal
    tipo: str
    descripcion: str = ""

    def validar(self) -> None:
        if self.cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero")
