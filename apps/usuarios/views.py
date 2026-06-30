from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from apps.usuarios.decorators import grupos_requeridos

from django.shortcuts import get_object_or_404


@login_required
@grupos_requeridos("Admin")
def usuarios_lista(request):
    usuarios = User.objects.all().order_by("-id")

    return render(request, "usuarios/lista.html", {
        "usuarios": usuarios
    })


@login_required
@grupos_requeridos("Admin")
def usuario_crear(request):
    grupos = Group.objects.all().order_by("name")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        email = request.POST.get("email")
        grupo_id = request.POST.get("grupo_id")

        usuario = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            email=email
        )

        if grupo_id:
            grupo = Group.objects.get(id=grupo_id)
            usuario.groups.add(grupo)

        messages.success(request, "Usuario creado correctamente")
        return redirect("usuarios:lista")

    return render(request, "usuarios/crear.html", {
        "grupos": grupos
    })



@login_required
@grupos_requeridos("Admin")
def usuario_editar(request, id):

    usuario = get_object_or_404(User, id=id)

    grupos = Group.objects.all().order_by("name")

    if request.method == "POST":

        usuario.first_name = request.POST.get("first_name")
        usuario.email = request.POST.get("email")

        grupo_id = request.POST.get("grupo_id")

        # LIMPIAR ROLES
        usuario.groups.clear()

        # NUEVO ROL
        if grupo_id:
            grupo = Group.objects.get(id=grupo_id)
            usuario.groups.add(grupo)

        usuario.save()

        messages.success(
            request,
            "Usuario actualizado correctamente"
        )

        return redirect("usuarios:lista")

    grupo_actual = usuario.groups.first()

    return render(request, "usuarios/editar.html", {
        "usuario_obj": usuario,
        "grupos": grupos,
        "grupo_actual": grupo_actual,
    })

    
@login_required
@grupos_requeridos("Admin")
def usuario_estado(request, id):
    usuario = get_object_or_404(User, id=id)

    if not usuario.is_superuser:
        usuario.is_active = not usuario.is_active
        usuario.save()
        messages.success(request, "Estado del usuario actualizado")

    return redirect("usuarios:lista")




def login_view(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            return redirect("/")

        messages.error(
            request,
            "Usuario o contraseña incorrectos"
        )

    return render(request, "usuarios/login.html")


def logout_view(request):
    logout(request)

    return redirect("usuarios:login")