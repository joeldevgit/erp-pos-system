from django.urls import path
from apps.inventario import views

app_name = "inventario"

urlpatterns = [
    path("", views.inventario_inicio, name="inventario_inicio"),

    path("mermas/", views.merma_list, name="merma_list"),
    path("mermas/crear/", views.merma_create, name="merma_create"),
    path("api/sync/mermas/", views.mermas_sync, name="mermas_sync"),
]