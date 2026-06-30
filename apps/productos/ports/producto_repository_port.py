from abc import ABC, abstractmethod

class ProductoRepositoryPort(ABC):
    @abstractmethod
    def obtener_por_id(self, producto_id):
        pass
