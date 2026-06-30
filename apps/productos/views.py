import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.core.permissions import permiso_requerido
from apps.productos.forms import (
    ProductoForm,
    PrecioAdicionalFormSet,
    CaducidadProductoFormSet,
)
from apps.productos.models import Producto
from apps.productos.repositories.producto_repository import ProductoRepository
from apps.productos.services.producto_service import (
    obtener_o_crear_categoria,
    obtener_o_crear_unidad,
)
from apps.productos.dto import ProductoData
from apps.productos.usecases.crear_producto_usecase import CrearProductoUseCase
from apps.productos.usecases.actualizar_producto_usecase import ActualizarProductoUseCase
from apps.productos.usecases.cambiar_estado_producto_usecase import CambiarEstadoProductoUseCase
from apps.productos.usecases.eliminar_producto_usecase import EliminarProductoUseCase
from apps.productos.usecases.sync_producto_usecase import SyncProductoUseCase


@login_required
def producto_list(request):
    return redirect("inventario:inventario_inicio")


@login_required
@permiso_requerido("productos.crear")
def producto_create(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)

        precios_formset = PrecioAdicionalFormSet(
            request.POST,
            prefix="precios_adicionales"
        )

        caducidades_formset = CaducidadProductoFormSet(
            request.POST,
            prefix="caducidades"
        )

        if form.is_valid() and precios_formset.is_valid() and caducidades_formset.is_valid():
            CrearProductoUseCase.ejecutar(
                form=form,
                data=ProductoData.from_form(form),
                precios_formset=precios_formset,
                caducidades_formset=caducidades_formset,
                usuario=request.user
            )

            messages.success(request, "Producto creado correctamente.")
            return redirect("/inventario/?seccion=producto")

    else:
        form = ProductoForm()

        precios_formset = PrecioAdicionalFormSet(
            prefix="precios_adicionales"
        )

        caducidades_formset = CaducidadProductoFormSet(
            prefix="caducidades"
        )

    productos = ProductoRepository.listar_todos()

    return render(request, "productos/crear.html", {
        "form": form,
        "precios_formset": precios_formset,
        "caducidades_formset": caducidades_formset,
        "productos": productos,
        "titulo": "Nuevo producto",
    })


@login_required
@permiso_requerido("productos.editar")
def producto_edit(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == "POST":
        form = ProductoForm(
            request.POST,
            request.FILES,
            instance=producto
        )

        precios_formset = PrecioAdicionalFormSet(
            request.POST,
            instance=producto,
            prefix="precios_adicionales"
        )

        caducidades_formset = CaducidadProductoFormSet(
            request.POST,
            instance=producto,
            prefix="caducidades"
        )

        if form.is_valid() and precios_formset.is_valid() and caducidades_formset.is_valid():
            ActualizarProductoUseCase.ejecutar(
                form=form,
                producto=producto,
                data=ProductoData.from_form(form),
                precios_formset=precios_formset,
                caducidades_formset=caducidades_formset,
                usuario=request.user
            )

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({
                    "ok": True,
                    "precios_ids": [
                        {"prefix": f.prefix, "id": f.instance.id}
                        for f in precios_formset.forms
                        if f.instance.id
                    ],
                    "caducidades_ids": [
                        {"prefix": f.prefix, "id": f.instance.id}
                        for f in caducidades_formset.forms
                        if f.instance.id
                    ],
                })

            messages.success(request, "Producto actualizado correctamente.")
            return redirect("/inventario/?seccion=producto")

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({
                "ok": False,
                "form_errors": form.errors.as_json(),
                "precios_errors": [e for e in precios_formset.errors],
                "caducidades_errors": [e for e in caducidades_formset.errors],
            }, status=400)

    else:
        form = ProductoForm(instance=producto)

        precios_formset = PrecioAdicionalFormSet(
            instance=producto,
            prefix="precios_adicionales"
        )

        caducidades_formset = CaducidadProductoFormSet(
            instance=producto,
            prefix="caducidades"
        )

    return render(request, "productos/editar.html", {
        "form": form,
        "producto": producto,
        "precios_formset": precios_formset,
        "caducidades_formset": caducidades_formset,
        "titulo": "Editar producto",
    })


@login_required
@permiso_requerido("productos.eliminar")
def producto_delete(request, id):
    producto = get_object_or_404(Producto, id=id)

    try:
        EliminarProductoUseCase.ejecutar(
            producto=producto,
            usuario=request.user
        )

        messages.success(request, "Producto eliminado correctamente.")

    except ProtectedError:
        messages.error(
            request,
            "No se puede eliminar porque está siendo usado."
        )

    return redirect("/inventario/?seccion=producto")


@login_required
@permiso_requerido("productos.cambiar_estado")
def producto_toggle_estado(request, id):
    producto = get_object_or_404(Producto, id=id)

    CambiarEstadoProductoUseCase.ejecutar(
        producto=producto,
        usuario=request.user
    )

    return redirect("inventario:producto_list")


@login_required
@permiso_requerido("productos.crear")
@require_POST
def crear_unidad_ajax(request):
    data = json.loads(request.body)
    nombre = data.get("nombre", "").strip()

    if not nombre:
        return JsonResponse({
            "ok": False,
            "error": "Nombre requerido"
        })

    unidad = obtener_o_crear_unidad(nombre)

    return JsonResponse({
        "ok": True,
        "id": unidad.id,
        "nombre": unidad.nombre
    })


@login_required
@permiso_requerido("productos.crear")
@require_POST
def crear_categoria_ajax(request):
    data = json.loads(request.body)
    nombre = data.get("nombre", "").strip()

    if not nombre:
        return JsonResponse({
            "ok": False,
            "error": "Nombre requerido"
        })

    categoria = obtener_o_crear_categoria(nombre)

    return JsonResponse({
        "ok": True,
        "id": categoria.id,
        "nombre": categoria.nombre
    })


@login_required
@permiso_requerido("productos.crear")
@require_POST
def productos_sync(request):
    try:
        data = json.loads(request.body)
    except Exception:
        return JsonResponse({
            "ok": False,
            "error": "JSON inválido"
        }, status=400)

    items = data if isinstance(data, list) else [data]
    results = []

    for item in items:
        client_id = item.get("client_id")

        try:
            producto, status = SyncProductoUseCase.ejecutar(
                item,
                usuario=request.user
            )

            results.append({
                "client_id": client_id,
                "status": status,
                "id": producto.id
            })

        except Exception as e:
            results.append({
                "client_id": client_id,
                "status": "error",
                "error": str(e)
            })

    return JsonResponse({
        "ok": True,
        "results": results
    })