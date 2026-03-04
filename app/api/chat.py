from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.schemas.chat_schema import ChatRequest, ChatResponse, MensagemHistoricoResponse
from app.services.chat_service import ChatService
from app.repositories.chat_repository import ChatRepository

router = APIRouter(prefix="/processos", tags=["Especialista IA (Chat)"])

@router.post("/{processo_id}/chat", response_model=ChatResponse, status_code=200)
async def enviar_mensagem_chat(
    processo_id: int, 
    request: ChatRequest, 
    db: AsyncSession = Depends(get_db)
):
    """
    Envia mensagem para IA mantendo o contexto do processo.
    """
    resposta_texto = await ChatService.enviar_mensagem(
        db=db, 
        processo_id=processo_id, 
        mensagem_usuario=request.mensagem
    )
    return {"resposta": resposta_texto}

@router.get("/{processo_id}/chat", response_model=List[MensagemHistoricoResponse], status_code=200)
async def listar_historico_chat(
    processo_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """
    Retorna todo o histórico de conversas daquele processo específico.
    """
    historico = await ChatRepository.buscar_historico(db=db, processo_id=processo_id)
    return historico