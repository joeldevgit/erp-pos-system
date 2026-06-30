from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from django.db.models.functions import TruncDate
from django.contrib.auth.decorators import login_required

from datetime import timedelta
import json

from apps.productos.models import Producto
# from apps.materia_primas.models import MateriaPrima
# from apps.servicios.models import Servicio

from apps.inventario.models import (
    MermaProducto,
    StockProducto,
)

# from apps.ventas.models import Venta
from apps.usuarios.decorators import grupos_requeridos


@login_required
@grupos_requeridos("Admin", "Cajero", "Vendedor")
def dashboard(request):
    hoy = timezone.now().date()

    total_productos = Producto.objects.filter(estado=True).count()
    # total_materias = MateriaPrima.objects.filter(estado=True).count()
    # total_servicios = Servicio.objects.filter(estado=True).count()

    productos_stock_bajo = StockProducto.objects.filter(
        cantidad__lte=5,
        producto__estado=True
    ).count()

    stock_bajo = productos_stock_bajo

    # ventas_hoy = Venta.objects.filter(
    #     fecha__date=hoy,
    #     activa=True
    # )

    # total_ventas_hoy = ventas_hoy.count()

    # monto_ventas_hoy = ventas_hoy.aggregate(
    #     total=Sum("total")
    # )["total"] or 0

    # ultimas_ventas = Venta.objects.order_by("-fecha")[:5]

    ultimas_mermas = MermaProducto.objects.order_by("-fecha")[:5]

    fecha_inicio = hoy - timedelta(days=6)

    # ventas_grafico = (
    #     Venta.objects.filter(
    #         fecha__date__gte=fecha_inicio,
    #         activa=True
    #     )
    #     .annotate(dia=TruncDate("fecha"))
    #     .values("dia")
    #     .annotate(total=Sum("total"))
    #     .order_by("dia")
    # )

    labels = []
    data = []

    # for venta in ventas_grafico:
    #     labels.append(venta["dia"].strftime("%d/%m"))
    #     data.append(float(venta["total"] or 0))

    return render(request, "inicio/dashboard.html", {
        "total_productos": total_productos,
        # "total_materias": total_materias,
        # "total_servicios": total_servicios,
        "stock_bajo": stock_bajo,
        "productos_stock_bajo": productos_stock_bajo,
        # "total_ventas_hoy": total_ventas_hoy,
        # "monto_ventas_hoy": monto_ventas_hoy,
        # "ultimas_ventas": ultimas_ventas,
        "ultimas_mermas": ultimas_mermas,
        "labels": json.dumps(labels),
        "data": json.dumps(data),
    })