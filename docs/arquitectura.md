# Arquitectura del Proyecto

## Patrón General

El proyecto utiliza una arquitectura basada en capas:

* Views
* Services
* Selectors
* Models

## Responsabilidades

### Views

Reciben requests HTTP y devuelven respuestas.

### Services

Contienen la lógica de negocio.

### Selectors

Centralizan consultas complejas a la base de datos.

### Models

Representan entidades persistentes.

## Auditoría

Todas las operaciones críticas se registran mediante AuditLog.

## Permisos

Los permisos se controlan mediante decorators y permissions.py.

## Eventos de Dominio

Los eventos se publican desde core/events.py para desacoplar procesos internos.

## Testing

Se utilizan pruebas unitarias y de integración con pytest.

## Objetivo

Mantener una arquitectura escalable, mantenible y desacoplada para un ERP/POS empresarial.
