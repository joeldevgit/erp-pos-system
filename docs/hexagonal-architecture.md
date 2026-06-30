# Hexagonal Architecture aplicada

Estructura agregada para separar reglas de negocio, casos de uso y Django:

```text
apps/productos/
  domain/            # Entidades y contratos/puertos
  application/       # UseCases
  infrastructure/    # Adaptadores Django ORM
  repositories/      # Repositorios existentes reutilizados

apps/inventario/
  domain/
  application/
  infrastructure/
```

## Flujo recomendado

```text
View / API Serializer
   -> Application UseCase
      -> Domain Entity / reglas
      -> Repository Port
         -> Infrastructure Adapter Django ORM
```

Ejemplo implementado:

```python
CrearProductoHexagonalUseCase(DjangoProductoRepository()).ejecutar(entity)
```

Esto permite que el caso de uso no dependa de `request`, templates ni serializers.
