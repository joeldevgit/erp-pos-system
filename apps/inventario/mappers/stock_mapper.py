from apps.inventario.domain.entities import MovimientoStockEntity


class StockMapper:
    """Convierte modelos de Django a entidades/diccionarios de inventario."""

    @staticmethod
    def movimiento_model_to_entity(model):
        return MovimientoStockEntity(
            producto_id=model.producto_id,
            cantidad=model.cantidad,
            tipo=model.tipo,
            descripcion=model.descripcion or "",
        )

    @staticmethod
    def stock_model_to_dict(model):
        return {
            "id": model.id,
            "producto_id": model.producto_id,
            "almacen_id": model.almacen_id,
            "cantidad": model.cantidad,
        }

    @staticmethod
    def movimiento_entity_to_dict(entity):
        return {
            "producto_id": entity.producto_id,
            "cantidad": entity.cantidad,
            "tipo": entity.tipo,
            "descripcion": entity.descripcion,
        }
