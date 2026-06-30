# ADR 0004 - PostgreSQL en producción

## Estado
Aceptado

## Contexto
SQLite es útil para desarrollo, pero no es ideal para producción multiusuario.

## Decisión
Usar PostgreSQL en producción mediante `DATABASE_URL`.

## Consecuencias
Mejor concurrencia, transacciones más robustas y despliegue más cercano a sistemas empresariales.
