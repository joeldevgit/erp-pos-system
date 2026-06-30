from django.test import TestCase

from apps.productos.models import Categoria, Unidad
from apps.productos.services.producto_service import obtener_o_crear_categoria, obtener_o_crear_unidad


class ProductoServiceTest(TestCase):
    def test_obtener_o_crear_categoria_normaliza_nombre(self):
        categoria = obtener_o_crear_categoria("  tecnologia  ")
        self.assertIsInstance(categoria, Categoria)
        self.assertEqual(categoria.nombre, "Tecnologia")

    def test_obtener_o_crear_unidad_normaliza_nombre(self):
        unidad = obtener_o_crear_unidad("  unidad  ")
        self.assertIsInstance(unidad, Unidad)
        self.assertEqual(unidad.nombre, "Unidad")

    def test_nombre_vacio_retorna_none(self):
        self.assertIsNone(obtener_o_crear_categoria(""))
        self.assertIsNone(obtener_o_crear_unidad(""))
