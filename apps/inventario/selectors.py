from apps.inventario.repositories.inventario_repository import MermaRepository


def listar_mermas():
    return MermaRepository.listar()