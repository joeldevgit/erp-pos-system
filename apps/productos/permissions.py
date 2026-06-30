"""Permisos funcionales de la app productos.

Mantener estos nombres centralizados evita strings sueltos en views, APIs y tests.
"""

PRODUCTOS_VER = "productos.ver"
PRODUCTOS_CREAR = "productos.crear"
PRODUCTOS_EDITAR = "productos.editar"
PRODUCTOS_ELIMINAR = "productos.eliminar"
PRODUCTOS_CAMBIAR_ESTADO = "productos.cambiar_estado"

PRODUCTOS_PERMISOS = {
    "ver": PRODUCTOS_VER,
    "crear": PRODUCTOS_CREAR,
    "editar": PRODUCTOS_EDITAR,
    "eliminar": PRODUCTOS_ELIMINAR,
    "cambiar_estado": PRODUCTOS_CAMBIAR_ESTADO,
}
