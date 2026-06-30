class ProductoError(Exception):
    """Error base de dominio/aplicación de productos."""


class ProductoInvalidoError(ProductoError):
    """Datos de producto inválidos para ejecutar una regla de negocio."""
