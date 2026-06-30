from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APIClient

from apps.productos.models import Categoria, Producto, Unidad


def test_api_v2_status_publico(client):
    response = client.get("/api/v2/status/")
    assert response.status_code == 200
    body = response.json()
    assert body["version"] == "v2"
    assert body["status"] == "stable"
    assert "productos" in body["resources"]


def test_api_v1_y_v2_exponen_productos_versionados(db):
    user = get_user_model().objects.create_user(username="versionuser", password="pass12345")
    user.groups.add(Group.objects.create(name="Admin"))
    categoria = Categoria.objects.create(nombre="Version Cat")
    unidad = Unidad.objects.create(nombre="Unidad", abreviatura="UND")
    Producto.objects.create(
        nombre="Producto Versionado",
        codigo="VER-001",
        categoria=categoria,
        unidad=unidad,
        precio_compra=Decimal("10.00"),
        precio_venta=Decimal("15.00"),
    )

    client = APIClient()
    client.force_authenticate(user=user)

    v1 = client.get("/api/v1/productos/")
    v2 = client.get("/api/v2/productos/")

    assert v1.status_code == 200
    assert v2.status_code == 200
    assert v1.data["results"][0]["codigo"] == "VER-001"
    assert v2.data["results"][0]["codigo"] == "VER-001"
