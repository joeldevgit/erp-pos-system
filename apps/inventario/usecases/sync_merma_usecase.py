from apps.inventario.dto import MermaData
from apps.inventario.forms import MermaProductoForm
from apps.inventario.usecases.registrar_merma_usecase import RegistrarMermaUseCase


class SyncMermaUseCase:

    @staticmethod
    def ejecutar(item, usuario=None):
        form = MermaProductoForm(item)

        if not form.is_valid():
            return {
                "client_id": item.get("client_id"),
                "status": "error",
                "errors": form.errors,
            }

        merma = form.save(commit=False)

        try:
            merma_creada = RegistrarMermaUseCase.ejecutar(
                producto=merma.producto,
                cantidad=merma.cantidad,
                motivo=merma.motivo,
                usuario=usuario
            )

            return {
                "client_id": item.get("client_id"),
                "status": "created",
                "id": merma_creada.id,
            }

        except Exception as e:
            return {
                "client_id": item.get("client_id"),
                "status": "error",
                "errors": str(e),
            }

            return {"client_id": item.get("client_id"), "status": "error", "errors": form.errors}

        try:
            merma_creada = RegistrarMermaUseCase.ejecutar(
                data=MermaData.from_form(form, usuario=usuario)
            )
            return {"client_id": item.get("client_id"), "status": "created", "id": merma_creada.id}
        except Exception as e:
            return {"client_id": item.get("client_id"), "status": "error", "errors": str(e)}
