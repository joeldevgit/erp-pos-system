"""DTOs de aplicación para desacoplar Django Forms/Serializers de los casos de uso.

La vista o serializer puede construir estos objetos, pero la lógica de negocio
no necesita conocer request.POST, ModelForm ni DRF directamente.
"""
from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from apps.productos.domain.entities import ProductoEntity


@dataclass(frozen=True)
class ProductoData:
    nombre: str
    precio_compra: Decimal
    precio_venta: Decimal
    codigo: str | None = None
    categoria: Any | None = None
    unidad: Any | None = None
    stock: Decimal | None = Decimal("0")
    stock_minimo: Decimal | None = Decimal("0")
    informacion_adicional: str = ""
    estado: bool = True
    imagen: Any | None = None

    @classmethod
    def from_form(cls, form):
        data = form.cleaned_data
        return cls(
            nombre=data.get("nombre"),
            imagen=data.get("imagen"),
            codigo=data.get("codigo"),
            categoria=data.get("categoria"),
            unidad=data.get("unidad"),
            precio_compra=data.get("precio_compra"),
            precio_venta=data.get("precio_venta"),
            stock=data.get("stock") or Decimal("0"),
            stock_minimo=data.get("stock_minimo") or Decimal("0"),
            informacion_adicional=data.get("informacion_adicional") or "",
            estado=data.get("estado", True),
        )

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            nombre=data.get("nombre"),
            imagen=data.get("imagen"),
            codigo=data.get("codigo"),
            categoria=data.get("categoria"),
            unidad=data.get("unidad"),
            precio_compra=data.get("precio_compra"),
            precio_venta=data.get("precio_venta"),
            stock=data.get("stock") or Decimal("0"),
            stock_minimo=data.get("stock_minimo") or Decimal("0"),
            informacion_adicional=data.get("informacion_adicional") or "",
            estado=data.get("estado", True),
        )

    def to_entity(self) -> ProductoEntity:
        return ProductoEntity(
            nombre=self.nombre,
            precio_compra=self.precio_compra,
            precio_venta=self.precio_venta,
            codigo=self.codigo,
            stock=self.stock,
            estado=self.estado,
        )

    def to_model_dict(self) -> dict:
        return {
            "nombre": self.nombre,
            "imagen": self.imagen,
            "codigo": self.codigo,
            "categoria": self.categoria,
            "unidad": self.unidad,
            "precio_compra": self.precio_compra,
            "precio_venta": self.precio_venta,
            "stock": self.stock,
            "stock_minimo": self.stock_minimo,
            "informacion_adicional": self.informacion_adicional,
            "estado": self.estado,
        }
