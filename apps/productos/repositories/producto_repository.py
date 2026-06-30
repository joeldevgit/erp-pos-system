from apps.productos.models import Producto, Categoria, Unidad


class ProductoRepository:

    @staticmethod
    def listar_todos():
        return Producto.objects.all().order_by("nombre")

    @staticmethod
    def obtener_por_id(producto_id):
        return Producto.objects.get(id=producto_id)

    @staticmethod
    def buscar_por_codigo(codigo):
        if not codigo:
            return None
        return Producto.objects.filter(codigo=codigo).first()

    @staticmethod
    def buscar_por_datos(nombre, precio_compra, precio_venta):
        return Producto.objects.filter(
            nombre=nombre,
            precio_compra=precio_compra,
            precio_venta=precio_venta
        ).first()

    @staticmethod
    def crear(**data):
        return Producto.objects.create(**data)

    @staticmethod
    def guardar(producto, update_fields=None):
        producto.save(update_fields=update_fields)
        return producto
    

    @staticmethod
    def eliminar(producto):
        producto.delete()


class CategoriaRepository:

    @staticmethod
    def obtener_o_crear(nombre):
        categoria, _ = Categoria.objects.get_or_create(nombre=nombre)
        return categoria


class UnidadRepository:

    @staticmethod
    def obtener_o_crear(nombre):
        unidad, _ = Unidad.objects.get_or_create(nombre=nombre)
        return unidad