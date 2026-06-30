from django.db import models


class Almacen(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class StockProducto(models.Model):
    producto = models.ForeignKey(
        "productos.Producto",
        on_delete=models.PROTECT,
        related_name="stocks"
    )
    almacen = models.ForeignKey(Almacen, on_delete=models.PROTECT)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ("producto", "almacen")

    def __str__(self):
        return f"{self.producto.nombre} - {self.almacen.nombre}: {self.cantidad}"


class MovimientoProducto(models.Model):
    ENTRADA = "entrada"
    SALIDA = "salida"
    AJUSTE = "ajuste"
    MERMA = "merma"
    MANUFACTURA = "manufactura"

    TIPO_MOVIMIENTO = (
        (ENTRADA, "Entrada"),
        (SALIDA, "Salida"),
        (AJUSTE, "Ajuste"),
        (MERMA, "Merma"),
        (MANUFACTURA, "Manufactura"),
    )

    producto = models.ForeignKey(
        "productos.Producto",
        on_delete=models.PROTECT,
        related_name="movimientos_inventario"
    )
    almacen = models.ForeignKey(Almacen, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.producto.nombre} - {self.cantidad}"


class MermaProducto(models.Model):
    producto = models.ForeignKey(
        "productos.Producto",
        on_delete=models.CASCADE
    )
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    motivo = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Merma de {self.producto.nombre}"