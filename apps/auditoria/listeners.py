from apps.auditoria.services import registrar_auditoria


def auditar_producto_creado(evento):
    registrar_auditoria(
        accion="CREATE",
        app="productos",
        modelo="Producto",
        objeto_id=evento.data.get("producto_id"),
        descripcion=f"Evento: producto creado - {evento.data.get('nombre')}"
    )