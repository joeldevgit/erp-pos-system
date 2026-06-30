from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.auditoria.models import AuditLog
from apps.auditoria.services import registrar_auditoria


class AuditoriaServiceTest(TestCase):
    def test_registrar_auditoria(self):
        user = get_user_model().objects.create_user(username="auditor", password="pass12345")

        log = registrar_auditoria(
            usuario=user,
            accion="CREATE",
            app="productos",
            modelo="Producto",
            objeto_id=1,
            descripcion="Prueba de auditoría",
        )

        self.assertIsInstance(log, AuditLog)
        self.assertEqual(log.usuario, user)
        self.assertEqual(log.accion, "CREATE")
