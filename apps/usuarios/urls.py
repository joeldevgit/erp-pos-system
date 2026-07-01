from django.urls import path
from . import views

app_name = "usuarios"

urlpatterns = [
    path("", views.usuarios_lista, name="lista"),
    path("crear/", views.usuario_crear, name="crear"),
    path("editar/<int:id>/", views.usuario_editar, name="editar"),
    path("estado/<int:id>/", views.usuario_estado, name="estado"),


    path("login/", views.login_view, name="login"),  # POR ORDEN DE LOGIN_URL = "..."
    path("logout/", views.logout_view, name="logout"),

]


