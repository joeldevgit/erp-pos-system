"""DTOs de aplicación para inventario."""
from dataclasses import dataclass
from decimal import Decimal
from typing import Any


@dataclass(frozen=True)
class MovimientoStockData:
    producto: Any
    cantidad: Decimal
    tipo: str
    almacen: Any | None = None
    usuario: Any | None = None
    observacion: str = ""

    def validar(self) -> None:
        if self.producto is None:
            raise ValueError("El producto es obligatorio.")
        if Decimal(str(self.cantidad)) <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")


@dataclass(frozen=True)
class MermaData:
    producto: Any
    cantidad: Decimal
    motivo: str
    usuario: Any | None = None

    @classmethod
    def from_form(cls, form, *, usuario=None):
        data = form.cleaned_data
        return cls(
            producto=data.get("producto"),
            cantidad=data.get("cantidad"),
            motivo=data.get("motivo") or "",
            usuario=usuario,
        )

    def validar(self) -> None:
        if self.producto is None:
            raise ValueError("El producto es obligatorio.")
        if Decimal(str(self.cantidad)) <= 0:
            raise ValueError("La cantidad debe ser mayor a 0.")
        if not self.motivo.strip():
            raise ValueError("El motivo de la merma es obligatorio.")
