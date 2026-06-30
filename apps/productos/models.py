from django.db import models

class Unidad(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    abreviatura = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=150, db_index=True)

    imagen = models.ImageField(
        upload_to='productos/',
        blank=True,
        null=True
    )

    codigo = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        db_index=True
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    unidad = models.ForeignKey(
        Unidad,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    # OBLIGATORIOS
    precio_compra = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    precio_venta = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    # OPCIONALES
    stock = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    stock_minimo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    informacion_adicional = models.TextField(blank=True)

    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    




class PrecioAdicional(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="precios_adicionales")
    nombre = models.CharField(max_length=100)  # Ej: Mayorista, Delivery, Docena
    precio = models.DecimalField(max_digits=10, decimal_places=2)

class CaducidadProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="caducidades")
    lote = models.CharField(max_length=50, blank=True)
    fecha_caducidad = models.DateField()
    informacion = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )