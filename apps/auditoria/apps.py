from django.apps import AppConfig


class AuditoriaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.auditoria'

    def ready(self):
        from apps.core.events import registrar_listener
        from apps.auditoria.listeners import auditar_producto_creado

        registrar_listener(
            "producto.creado",
            auditar_producto_creado
        )