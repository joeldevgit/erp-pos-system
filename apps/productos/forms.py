from django import forms
from django.forms import inlineformset_factory
from apps.productos.models import Producto, PrecioAdicional, CaducidadProducto



# FORMULARIO DE PRODUCTO
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            "nombre", "imagen", "codigo", "categoria", "unidad",
            "precio_compra", "precio_venta",
            "stock", "stock_minimo",
            "informacion_adicional", "estado",
        ]
        widgets = {
            "nombre": forms.TextInput(attrs={
                "class": "form-control",
                "style": "text-transform: uppercase;"
            }),
            "imagen": forms.FileInput(attrs={
                "class": "form-control",
                "accept": "image/*",
                "id": "id_imagen",
            }),
            "codigo": forms.TextInput(attrs={
                "class": "form-control",
                "style": "text-transform: uppercase;"
            }),
            "categoria": forms.Select(attrs={"class": "form-control"}),
            "unidad": forms.Select(attrs={"class": "form-select"}),
            "precio_compra": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "precio_venta": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "stock": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "stock_minimo": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "informacion_adicional": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "estado": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get("nombre")

        if nombre:
            return nombre.upper()

        return nombre

    def clean_codigo(self):
        codigo = self.cleaned_data.get("codigo")

        if codigo:
            return codigo.upper()

        return None


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["codigo"].required = False


        
# PRECIOS ADICIONALES
PrecioAdicionalFormSet = inlineformset_factory(
    Producto,
    PrecioAdicional,
    fields=("nombre", "precio"),
    extra=0,
    can_delete=True
)




class CaducidadProductoForm(forms.ModelForm):
    fecha_caducidad = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control"
            },
            format="%Y-%m-%d"
        ),
        input_formats=["%Y-%m-%d"]
    )

    class Meta:
        model = CaducidadProducto
        fields = ("lote", "fecha_caducidad", "informacion")
        widgets = {
            "lote": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Lote"
            }),
            "informacion": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Información"
            }),
        }

# CADUCIDADES
CaducidadProductoFormSet = inlineformset_factory(
    Producto,
    CaducidadProducto,
    form=CaducidadProductoForm,
    extra=0,
    can_delete=True
)


