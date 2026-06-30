from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class ProductoActualizadoEvent:
    producto_id:int
    fecha:datetime
