from apps.productos.domain.entities import ProductoEntity
from apps.productos.models import Producto
from apps.productos.repositories.producto_repository import ProductoRepository


class DjangoProductoRepository(ProductoRepository):
    def crear_desde_entidad(self, entity: ProductoEntity):
        return Producto.objects.create(
            nombre=entity.nombre.strip(),
            codigo=entity.codigo,
            precio_compra=entity.precio_compra,
            precio_venta=entity.precio_venta,
            stock=entity.stock,
            estado=entity.estado,
        )
