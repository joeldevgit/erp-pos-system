# ADR 0003 - Auditoría y eventos de dominio

## Estado
Aceptado

## Contexto
Un ERP/POS necesita trazabilidad sobre cambios importantes.

## Decisión
Usar auditoría centralizada y eventos de dominio para acciones relevantes como creación de productos, cambios de stock y mermas.

## Consecuencias
Se puede revisar qué ocurrió, cuándo ocurrió y quién ejecutó la acción. También permite agregar listeners sin modificar la lógica principal.
