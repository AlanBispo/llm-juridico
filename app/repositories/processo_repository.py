from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.processo_model import ProcessoModel
from app.schemas.processo_schema import ProcessoCreate

class ProcessoRepository:
    
    @staticmethod
    async def buscar_por_numero(db: AsyncSession, numero: str) -> ProcessoModel | None:
        """
        Busca um processo judicial específico pelo número padrão CNJ.
        Retorna o modelo do banco ou None se não existir.
        """
        stmt = select(ProcessoModel).where(ProcessoModel.numero == numero)
        
        resultado = await db.execute(stmt)
        
        return resultado.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, processo: ProcessoCreate) -> ProcessoModel:
        """
        Insere um novo processo no banco de dados.
        """
        db_processo = ProcessoModel(**processo.model_dump())
        
        db.add(db_processo)
        await db.commit()
        await db.refresh(db_processo)
        
        return db_processo
    
    @staticmethod
    async def get_all(db: AsyncSession, skip: int = 0, limit: int = 100):
        stmt = select(ProcessoModel).offset(skip).limit(limit)
        result = await db.execute(stmt)

        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, processo_id: int) -> ProcessoModel | None:
        stmt = select(ProcessoModel).where(ProcessoModel.id == processo_id)
        result = await db.execute(stmt)

        return result.scalars().first()

    @staticmethod
    async def get_by_numero(db: AsyncSession, numero: str) -> ProcessoModel | None:
        stmt = select(ProcessoModel).where(ProcessoModel.numero == numero)
        result = await db.execute(stmt)
        
        return result.scalars().first()