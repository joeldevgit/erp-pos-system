from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ProductoEntity:
    nombre: str
    precio_compra: Decimal
    precio_venta: Decimal
    codigo: str | None = None
    stock: Decimal | None = None
    estado: bool = True

    def validar(self) -> None:
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del producto es obligatorio")
        if self.precio_compra < 0 or self.precio_venta < 0:
            raise ValueError("Los precios no pueden ser negativos")
        if self.stock is not None and self.stock < 0:
            raise ValueError("El stock no puede ser negativo")
