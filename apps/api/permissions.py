from rest_framework.permissions import BasePermission, SAFE_METHODS


class RolModuloPermission(BasePermission):
    """
    Permiso por rol para la API.

    Regla senior:
    - superuser: acceso total
    - Admin/Administrador: lectura y escritura
    - Vendedor/Cajero: lectura
    - otros usuarios autenticados: sin acceso al módulo
    """

    roles_escritura = {"Admin", "Administrador", "Principal", "Administradora"}
    roles_lectura = roles_escritura | {"Vendedor", "Cajero"}

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        roles = set(user.groups.values_list("name", flat=True))

        if request.method in SAFE_METHODS:
            return bool(roles & self.roles_lectura)

        return bool(roles & self.roles_escritura)
