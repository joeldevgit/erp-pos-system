import json

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.utils import timezone

from apps.usuarios.decorators import grupos_requeridos

from apps.inventario.forms import MermaProductoForm
from apps.inventario.services.merma_service import registrar_merma
from apps.inventario.selectors import listar_mermas
from apps.productos.selectors import buscar_productos_activos

from apps.core.permissions import permiso_requerido




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
        merma = form.save(commit=False)

        try:
            registrar_merma(
                producto=merma.producto,
                cantidad=merma.cantidad,
                motivo=merma.motivo
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
        return JsonResponse({"ok": False, "error": "JSON inválido"}, status=400)

    items = data if isinstance(data, list) else [data]
    results = []

    for item in items:
        form = MermaProductoForm(item)

        if not form.is_valid():
            results.append({
                "client_id": item.get("client_id"),
                "status": "error",
                "errors": form.errors
            })
            continue

        merma = form.save(commit=False)

        try:
            merma_creada = registrar_merma(
                producto=merma.producto,
                cantidad=merma.cantidad,
                motivo=merma.motivo
            )
        except Exception as e:
            results.append({
                "client_id": item.get("client_id"),
                "status": "error",
                "errors": str(e)
            })
            continue

        results.append({
            "client_id": item.get("client_id"),
            "status": "created",
            "id": merma_creada.id
        })

    return JsonResponse({"ok": True, "results": results})