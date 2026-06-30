# Stock

## Objetivo

Centralizar la lógica de inventario para evitar inconsistencias.

## Servicios principales

- `entrada_stock()`
- `salida_stock()`
- `registrar_merma()`
- `obtener_stock_producto()`
- `registrar_movimiento()`

## Regla de negocio

El stock nunca debe quedar negativo. Toda salida valida cantidad disponible antes de guardar.

## Movimiento de inventario

Cada entrada, salida o merma debe generar un `MovimientoProducto`.

## Capas

```txt
View/API -> UseCase -> Service -> Repository/Model
```

La API no debe descontar stock directamente con `producto.stock -= cantidad`.
