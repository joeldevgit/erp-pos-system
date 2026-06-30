# Arquitectura Senior: productos e inventario

## Objetivo
Las apps `productos` e `inventario` siguen una separación por capas para evitar que las vistas, formularios o serializers contengan reglas de negocio.

## Capas

```text
interfaces: views, forms, serializers, urls
application: dto.py, usecases/
domain: entities.py, repositories.py, exceptions.py
infrastructure: repositories Django/ORM
```

## Reglas aplicadas

- Las vistas validan entrada HTTP y delegan a casos de uso.
- Los casos de uso reciben DTOs o entidades, no dependen directamente de `request.POST`.
- Los repositories concentran el acceso a datos.
- Los services contienen reglas reutilizables de dominio simple.
- Las operaciones críticas de stock y producto usan `transaction.atomic`.
- Auditoría y eventos de dominio se emiten desde la capa de aplicación.

## Productos

Flujo recomendado:

```text
ProductoForm / Serializer -> ProductoData -> Crear/ActualizarProductoUseCase -> Repository/ORM -> AuditLog/Event
```

## Inventario

Flujo recomendado:

```text
MermaProductoForm -> MermaData -> RegistrarMermaUseCase -> salida_stock -> MovimientoProducto + MermaProducto
```

## Convención

Los archivos `services/`, `repositories/`, `usecases/`, `dto.py`, `domain/` e `infrastructure/` deben mantenerse pequeños y con responsabilidad única.
