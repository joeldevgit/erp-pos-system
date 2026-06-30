from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class StockSalidaRegistradaEvent:
    producto_id: int
    cantidad: Decimal
    almacen_id: int | None
    fecha: datetime
