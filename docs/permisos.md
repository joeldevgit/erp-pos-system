# Permisos

## Objetivo

Controlar acceso por rol y por módulo.

## Roles principales

- Admin / Administrador / Principal / Administradora: lectura y escritura.
- Vendedor / Cajero: lectura en API.
- Superuser: acceso total.

## API

La API usa `RolModuloPermission` en `apps/api/permissions.py`.

Regla:

```txt
GET/HEAD/OPTIONS -> roles de lectura
POST/PUT/PATCH/DELETE -> roles administrativos
```

## Vistas HTML

Las vistas pueden usar decoradores de `apps/core/permissions.py` o decoradores de la app de usuarios.

## Recomendación

Cada módulo nuevo debe declarar permisos explícitos antes de exponerse en menú, vista o API.
