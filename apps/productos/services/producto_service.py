from apps.core.utils import normalizar_texto
from apps.productos.repositories.producto_repository import (
    CategoriaRepository,
    UnidadRepository,
)


def activar_producto(producto):
    producto.estado = True
    return producto


def cambiar_estado(producto):
    producto.estado = not producto.estado
    return producto


def obtener_o_crear_categoria(nombre):
    nombre = normalizar_texto(nombre)

    if not nombre:
        return None

    return CategoriaRepository.obtener_o_crear(nombre)


def obtener_o_crear_unidad(nombre):
    nombre = normalizar_texto(nombre)

    if not nombre:
        return None

    return UnidadRepository.obtener_o_crear(nombre)