from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from django.contrib.auth.models import AnonymousUser, Group, User
from django.test import RequestFactory

from apps.api.permissions import RolModuloPermission
from apps.core.permissions import usuario_tiene_permiso, permiso_requerido
from apps.core.utils import es_ajax, normalizar_texto


@pytest.mark.django_db
def test_usuario_tiene_permiso_por_grupo():
    user = User.objects.create_user(username="admin")
    group = Group.objects.create(name="Admin")
    user.groups.add(group)

    assert usuario_tiene_permiso(user, "productos.crear") is True
    assert usuario_tiene_permiso(user, "permiso.inexistente") is False


def test_usuario_anonimo_no_tiene_permiso():
    assert usuario_tiene_permiso(AnonymousUser(), "productos.crear") is False


@pytest.mark.django_db
def test_permiso_requerido_permite_view(rf):
    user = User.objects.create_user(username="seller")
    group = Group.objects.create(name="Vendedor")
    user.groups.add(group)
    request = rf.get("/")
    request.user = user

    view = permiso_requerido("productos.crear")(lambda request: "ok")

    assert view(request) == "ok"


@pytest.mark.django_db
def test_api_permission_superuser_y_roles(rf):
    permission = RolModuloPermission()
    view = SimpleNamespace()
    request = rf.post("/api/v1/productos/")
    request.user = User.objects.create_superuser(username="root", password="x")
    assert permission.has_permission(request, view) is True

    normal_user = User.objects.create_user(username="reader")
    normal_user.groups.add(Group.objects.create(name="Cajero"))
    request = rf.get("/api/v1/productos/")
    request.user = normal_user
    assert permission.has_permission(request, view) is True

    request = rf.post("/api/v1/productos/")
    request.user = normal_user
    assert permission.has_permission(request, view) is False


def test_api_permission_anonimo(rf):
    request = rf.get("/api/v1/productos/")
    request.user = AnonymousUser()
    assert RolModuloPermission().has_permission(request, SimpleNamespace()) is False


def test_utils_normalizar_y_ajax(rf):
    request = rf.get("/", HTTP_X_REQUESTED_WITH="XMLHttpRequest")
    assert normalizar_texto("  tecnologia avanzada ") == "Tecnologia Avanzada"
    assert es_ajax(request) is True
    assert es_ajax(rf.get("/")) is False
