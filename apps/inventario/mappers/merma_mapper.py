class MermaMapper:
    """Convierte mermas entre modelo Django y estructuras simples."""

    @staticmethod
    def model_to_dict(model):
        return {
            "id": model.id,
            "producto_id": model.producto_id,
            "cantidad": model.cantidad,
            "motivo": model.motivo,
            "fecha": model.fecha,
        }
