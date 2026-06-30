from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class ProductoEliminadoEvent:
    producto_id:int
    fecha:datetime
