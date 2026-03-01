from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.processo_schema import ProcessoCreate, ProcessoUpdate
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
    
    @staticmethod
    async def listar_processos(db: AsyncSession, skip: int = 0, limit: int = 100):
        return await ProcessoRepository.get_all(db=db, skip=skip, limit=limit)

    @staticmethod
    async def obter_processo_por_id(db: AsyncSession, processo_id: int):
        processo = await ProcessoRepository.get_by_id(db=db, processo_id=processo_id)
        
        if not processo:
            raise HTTPException(status_code=404, detail="Processo não encontrado.")
            
        return processo
    
    @staticmethod
    async def atualizar_processo(db: AsyncSession, processo_id: int, processo_in: ProcessoUpdate):
        # Verifica se o processo existe
        db_processo = await ProcessoRepository.get_by_id(db=db, processo_id=processo_id)
        if not db_processo:
            raise HTTPException(status_code=404, detail="Processo não encontrado para atualização.")
        
        # Verifica número CNJ duplicado.
        if processo_in.numero and processo_in.numero != db_processo.numero:
            processo_existente = await ProcessoRepository.get_by_numero(db=db, numero=processo_in.numero)
            if processo_existente:
                raise HTTPException(
                    status_code=400, 
                    detail="Já existe outro processo cadastrado com este novo número CNJ."
                )

        return await ProcessoRepository.update(db=db, db_processo=db_processo, processo_in=processo_in)