class InventarioError(Exception):
    """Error base de inventario."""


class MovimientoInventarioInvalidoError(InventarioError):
    """Movimiento de inventario inválido."""
