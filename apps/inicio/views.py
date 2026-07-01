from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from django.db.models.functions import TruncDate
from django.contrib.auth.decorators import login_required

from datetime import timedelta
import json

from apps.productos.models import Producto

from apps.inventario.models import (
    MermaProducto,
    StockProducto,
)

from apps.usuarios.decorators import grupos_requeridos


@login_required  # ¿ESTÁ AUTENTICADO?
@grupos_requeridos("Admin", "Empleado") # SI ESTÁ AUTENTICADO, ¿PERTENECE A ALGUNO DE LOS GRUPOS?
def dashboard(request):
    hoy = timezone.now().date()

    total_productos = Producto.objects.filter(
        estado=True
    ).count()

    productos_stock_bajo = StockProducto.objects.filter(
        cantidad__lte=5,
        producto__estado=True
    ).count()

    stock_bajo = productos_stock_bajo

    ultimas_mermas = MermaProducto.objects.order_by("-fecha")[:5]

    fecha_inicio = hoy - timedelta(days=6)

    labels = []
    data = []

    return render(request, "inicio/dashboard.html", {
        "total_productos": total_productos,
        "stock_bajo": stock_bajo,
        "productos_stock_bajo": productos_stock_bajo,
        "ultimas_mermas": ultimas_mermas,
        "labels": json.dumps(labels),
        "data": json.dumps(data),
    })