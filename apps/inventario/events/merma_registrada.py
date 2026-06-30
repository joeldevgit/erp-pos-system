from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class MermaRegistradaEvent:
    producto_id: int
    cantidad: Decimal
    motivo: str
    fecha: datetime
