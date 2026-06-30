from decimal import Decimal

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from rest_framework.test import APIClient

from apps.auditoria.models import AuditLog
from apps.productos.models import Categoria, Producto, Unidad


class ProductoAPITest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="apiuser", password="pass12345")
        self.admin_group = Group.objects.create(name="Admin")
        self.user.groups.add(self.admin_group)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.categoria = Categoria.objects.create(nombre="Tecnología")
        self.unidad = Unidad.objects.create(nombre="Unidad", abreviatura="UND")

    def test_lista_productos_autenticado(self):
        Producto.objects.create(
            nombre="Laptop",
            codigo="LAP-001",
            categoria=self.categoria,
            unidad=self.unidad,
            precio_compra=Decimal("1000.00"),
            precio_venta=Decimal("1200.00"),
            stock=Decimal("5.00"),
            estado=True,
        )

        response = self.client.get("/api/v1/productos/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["results"][0]["nombre"], "Laptop")

    def test_crea_producto_autenticado_usando_usecase_y_auditoria(self):
        payload = {
            "nombre": "Mouse",
            "codigo": "MOU-001",
            "categoria": self.categoria.id,
            "unidad": self.unidad.id,
            "precio_compra": "20.00",
            "precio_venta": "35.00",
            "stock": "10.00",
            "stock_minimo": "2.00",
            "informacion_adicional": "",
            "estado": True,
        }

        response = self.client.post("/api/v1/productos/", payload, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Producto.objects.filter(codigo="MOU-001").exists())
        self.assertTrue(AuditLog.objects.filter(modelo="Producto", accion="CREATE").exists())

    def test_usuario_sin_rol_no_puede_crear_producto(self):
        self.user.groups.clear()
        payload = {
            "nombre": "Sin permiso",
            "codigo": "SIN-001",
            "precio_compra": "1.00",
            "precio_venta": "2.00",
        }

        response = self.client.post("/api/v1/productos/", payload, format="json")

        self.assertEqual(response.status_code, 403)

    def test_vendedor_solo_puede_leer(self):
        self.user.groups.clear()
        self.user.groups.add(Group.objects.create(name="Vendedor"))

        get_response = self.client.get("/api/v1/productos/")
        post_response = self.client.post(
            "/api/v1/productos/",
            {"nombre": "Bloqueado", "precio_compra": "1.00", "precio_venta": "2.00"},
            format="json",
        )

        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(post_response.status_code, 403)
