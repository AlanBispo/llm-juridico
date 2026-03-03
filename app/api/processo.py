from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.processo_schema import ProcessoCreate, ProcessoResponse, ProcessoUpdate
from app.services.processo_service import ProcessoService

router = APIRouter(prefix="/processos", tags=["Processos"])

@router.post("/", status_code=201)
async def criar_processo(processo_in: ProcessoCreate, db: AsyncSession = Depends(get_db)):
    novo_processo = await ProcessoService.criar_processo(db=db, processo_in=processo_in)
    
    return novo_processo

@router.get("/", response_model=List[ProcessoResponse], status_code=200)
async def listar_processos(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await ProcessoService.listar_processos(db=db, skip=skip, limit=limit)

@router.get("/{processo_id}", response_model=ProcessoResponse, status_code=200)
async def obter_processo(processo_id: int, db: AsyncSession = Depends(get_db)):
    return await ProcessoService.obter_processo_por_id(db=db, processo_id=processo_id)

@router.put("/{processo_id}", response_model=ProcessoResponse, status_code=200)
async def atualizar_processo(processo_id: int, processo_in: ProcessoUpdate, db: AsyncSession = Depends(get_db)):
    return await ProcessoService.atualizar_processo(db=db, processo_id=processo_id, processo_in=processo_in)

@router.delete("/{processo_id}", status_code=204)
async def deletar_processo(processo_id: int, db: AsyncSession = Depends(get_db)):
    await ProcessoService.deletar_processo(db=db, processo_id=processo_id)
    
    return {"message": "Processo deletado com sucesso."}

@router.post("/{processo_id}/tese", response_model=ProcessoResponse, status_code=200)
async def gerar_tese(
    processo_id: int, 
    db: AsyncSession = Depends(get_db)
):
    processo_atualizado = await ProcessoService.gerar_tese_estrategica(db=db, processo_id=processo_id)
    return processo_atualizado
