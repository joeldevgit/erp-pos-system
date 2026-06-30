# Auditoría

## Objetivo

Registrar acciones importantes del sistema para trazabilidad empresarial.

## Acciones auditables

- CREATE
- UPDATE
- DELETE
- LOGIN
- LOGOUT
- STOCK

## Ubicación

- Modelo: `apps/auditoria/models.py`
- Servicio: `apps/auditoria/services.py`
- Listeners: `apps/auditoria/listeners.py`

## Regla senior

Las vistas, API y casos de uso no deben crear logs manuales duplicados. Deben llamar al servicio `registrar_auditoria()` o publicar un evento de dominio cuando corresponda.

## Ejemplo

```python
registrar_auditoria(
    usuario=request.user,
    accion="CREATE",
    app="productos",
    modelo="Producto",
    objeto_id=producto.id,
    descripcion="Se creó un producto",
)
```
