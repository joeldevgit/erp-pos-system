# ADR 0001 - Arquitectura por capas

## Estado
Aceptado

## Contexto
El sistema ERP/POS necesita ser mantenible, escalable y fácil de probar.

## Decisión
Se usará arquitectura por capas:

- Views: reciben requests
- Services: lógica de negocio
- Selectors: consultas
- Models: estructura de datos
- Events: eventos de dominio
- Auditoría: trazabilidad

## Consecuencias
El código será más ordenado, testeable y preparado para crecer.