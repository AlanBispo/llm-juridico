from fastapi import APIRouter, HTTPException
from app.services.juridico_service import JuridicoService

router = APIRouter()
service = JuridicoService()

@router.get("/{processo_id}")
async def triagem(processo_id: int):
    resultado = await service.executar_fluxo_triagem(processo_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Processo não encontrado")
    return resultado