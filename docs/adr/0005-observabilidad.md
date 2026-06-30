# ADR 0005 - Observabilidad

## Estado
Aceptado

## Contexto
En producción no basta con que el sistema funcione; se necesita saber cuándo falla, por qué falla y cómo se comporta.

## Decisión
Agregar:

- Sentry para errores.
- `django-prometheus` para métricas.
- Healthchecks `/health/` y `/ready/`.
- Logs por consola listos para plataformas cloud.

## Consecuencias
El sistema queda preparado para monitoreo real, alertas y diagnóstico de incidentes.
