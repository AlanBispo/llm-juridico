from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.processo_schema import ProcessoCreate
from app.services.processo_service import ProcessoService

router = APIRouter(prefix="/processos", tags=["Processos"])

@router.post("/", status_code=201)
async def criar_processo(processo_in: ProcessoCreate, db: AsyncSession = Depends(get_db)):
    novo_processo = await ProcessoService.criar_processo(db=db, processo_in=processo_in)
    
    return novo_processo