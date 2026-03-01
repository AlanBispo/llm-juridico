from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.processo_schema import ProcessoCreate, ProcessoResponse
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
