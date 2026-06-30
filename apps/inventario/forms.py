from django import forms
from apps.inventario.models import MermaProducto
from apps.productos.models import Producto


class MermaProductoForm(forms.ModelForm):
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.filter(stock__gt=0)
        .exclude(nombre__icontains="MANU")
        .order_by("nombre"),
        label="Producto",
        empty_label="Seleccione un producto",
        widget=forms.Select(attrs={"class": "producto-input"})
    )

    class Meta:
        model = MermaProducto
        fields = ["producto", "cantidad", "motivo"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["producto"].label_from_instance = (
            lambda obj: f"{obj.nombre} (Stock: {obj.stock})"
        )