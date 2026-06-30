from django.urls import path
from . import views

app_name = "productos"

urlpatterns = [
    path("", views.producto_list, name="producto_list"),
    path("crear/", views.producto_create, name="producto_create"),
    path("<int:id>/editar/", views.producto_edit, name="producto_edit"),
    path("eliminar/<int:id>/", views.producto_delete, name="producto_delete"),
    path("estado/<int:id>/", views.producto_toggle_estado, name="producto_toggle_estado"),

    path("unidad/ajax/crear/", views.crear_unidad_ajax, name="crear_unidad_ajax"),
    path("categoria/ajax/crear/", views.crear_categoria_ajax, name="crear_categoria_ajax"),
    path("api/sync/productos/", views.productos_sync, name="productos_sync"),
]