from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.processo_schema import ProcessoCreate
from app.repositories.processo_repository import ProcessoRepository

class ProcessoService:
    
    @staticmethod
    async def criar_processo(db: AsyncSession, processo_in: ProcessoCreate):
        processo_existente = await ProcessoRepository.buscar_por_numero(db, processo_in.numero)
        
        if processo_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Já existe um processo cadastrado com o número {processo_in.numero}."
            )
        
        processo_criado = await ProcessoRepository.create(db=db, processo=processo_in)
        
        return processo_criado