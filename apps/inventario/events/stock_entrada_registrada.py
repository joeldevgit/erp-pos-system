from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class StockEntradaRegistradaEvent:
    producto_id: int
    cantidad: Decimal
    almacen_id: int | None
    fecha: datetime
