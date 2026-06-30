# apps/core/exceptions.py

class BusinessError(Exception):
    pass


class StockInsuficienteError(BusinessError):
    pass


class CantidadInvalidaError(BusinessError):
    pass    