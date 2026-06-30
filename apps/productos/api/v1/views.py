from rest_framework.viewsets import ReadOnlyModelViewSet
from productos.models import Producto
from .serializers import ProductoSerializer

class ProductoViewSet(ReadOnlyModelViewSet):
    queryset=Producto.objects.all()
    serializer_class=ProductoSerializer
