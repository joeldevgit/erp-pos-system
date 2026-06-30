# ADR 0002 - Services y Selectors

## Estado
Aceptado

## Contexto
Las vistas con lógica de negocio se vuelven difíciles de mantener y probar.

## Decisión
Separar responsabilidades:

- Selectors: consultas y lectura.
- Services: reglas de negocio.
- UseCases: orquestación de operaciones completas.
- Views/API: entrada y salida HTTP.

## Consecuencias
El sistema gana testabilidad, mantenibilidad y menor acoplamiento.
