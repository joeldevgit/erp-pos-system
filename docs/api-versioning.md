# API Versioning avanzado

Rutas disponibles:

```text
/api/v1/      API estable actual
/api/v2/      API reservada para cambios incompatibles
/api/schema/  OpenAPI
/api/docs/    Swagger
/api/redoc/   ReDoc
```

Reglas:

1. `v1` mantiene compatibilidad.
2. `v2` se usa cuando cambian contratos de request/response.
3. No romper `v1` sin deprecation documentado.
4. Nuevos endpoints mayores deben vivir dentro de `apps/api/v2/`.
