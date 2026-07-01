from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect


PERMISOS_POR_ROL = {

    "Admin": [
        "inventario.ver",
        "inventario.mermas.ver",
        "inventario.mermas.crear",
        "inventario.stock.entrada",
        "inventario.stock.salida",

        "productos.ver",
        "productos.crear",
        "productos.editar",
        "productos.eliminar",
        "productos.cambiar_estado",


        # aquí irán ventas, compras, clientes, etc.
    ],

    "Empleado": [
        "inventario.ver",
        "inventario.mermas.ver",
        "inventario.mermas.crear",
        "inventario.stock.entrada",
        "inventario.stock.salida",

        "productos.ver",
        "productos.crear",
        "productos.editar",

        # sin permisos de usuarios
    ],
}


def usuario_tiene_permiso(usuario, permiso):
    if not usuario.is_authenticated:
        return False

    # Superusuario entra a todo
    if usuario.is_superuser:
        return True
    
    grupos = usuario.groups.values_list("name", flat=True)

    for grupo in grupos:
        permisos = PERMISOS_POR_ROL.get(grupo, [])

        if permiso in permisos:
            return True

    return False


def permiso_requerido(permiso):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if usuario_tiene_permiso(request.user, permiso):
                return view_func(request, *args, **kwargs)

            messages.error(request, "No tienes permiso para realizar esta acción.")
            return redirect("inventario:inventario_inicio")


        return wrapper
    return decorator