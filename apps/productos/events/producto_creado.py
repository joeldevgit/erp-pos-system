from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class ProductoCreadoEvent:
    producto_id:int
    nombre:str
    fecha:datetime
