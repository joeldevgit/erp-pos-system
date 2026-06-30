import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.core.permissions import permiso_requerido
from apps.inventario.dto import MermaData
from apps.inventario.forms import MermaProductoForm
from apps.inventario.selectors import listar_mermas
from apps.inventario.usecases.registrar_merma_usecase import RegistrarMermaUseCase
from apps.inventario.usecases.sync_merma_usecase import SyncMermaUseCase
from apps.productos.selectors import buscar_productos_activos


@login_required
@permiso_requerido("inventario.ver")
def inventario_inicio(request):
    seccion = request.GET.get("seccion", "producto")
    q = request.GET.get("q", "").strip()

    titulos = {
        "producto": "Productos",
        "servicio": "Servicios",
        "manufactura": "Manufactura",
    }

    if seccion not in titulos:
        seccion = "producto"

    productos = buscar_productos_activos(q)

    paginator = Paginator(productos, 16)
    page_number = request.GET.get("page")
    productos = paginator.get_page(page_number)

    return render(request, "inventario/inventario.html", {
        "productos": productos,
        "titulo": titulos[seccion],
        "seccion": seccion,
        "q": q,
    })


@login_required
@permiso_requerido("inventario.mermas.ver")
def merma_list(request):
    mermas = listar_mermas()

    return render(request, "inventario/mermas/productos/lista.html", {
        "mermas": mermas,
        "titulo": "Merma"
    })


@login_required
@permiso_requerido("inventario.mermas.crear")
def merma_create(request):
    form = MermaProductoForm(request.POST or None)

    productos_costos = {
        str(p.id): float(p.precio_compra or 0)
        for p in form.fields["producto"].queryset
    }

    if request.method == "POST" and form.is_valid():
        try:
            RegistrarMermaUseCase.ejecutar(
                data=MermaData.from_form(form, usuario=request.user)
            )

        except Exception as e:
            messages.error(request, str(e))
            return redirect("inventario:merma_create")

        messages.success(request, "Merma registrada correctamente.")
        return redirect("inventario:merma_list")

    return render(request, "inventario/mermas/productos/crear.html", {
        "form": form,
        "fecha_actual": timezone.localtime(),
        "productos_costos": productos_costos,
    })


@login_required
@permiso_requerido("inventario.mermas.crear")
@require_POST
def mermas_sync(request):
    try:
        data = json.loads(request.body)

    except Exception:
        return JsonResponse({
            "ok": False,
            "error": "JSON inválido"
        }, status=400)

    items = data if isinstance(data, list) else [data]

    results = [
        SyncMermaUseCase.ejecutar(
            item,
            usuario=request.user
        )
        for item in items
    ]

    return JsonResponse({
        "ok": True,
        "results": results
    })