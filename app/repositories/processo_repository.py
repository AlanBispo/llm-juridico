from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.processo_model import ProcessoModel
from app.schemas.processo_schema import ProcessoCreate, ProcessoUpdate

class ProcessoRepository:
    
    @staticmethod
    async def get_by_number(db: AsyncSession, number: str) -> ProcessoModel | None:
        stmt = select(ProcessoModel).where(ProcessoModel.numero == number)
        result = await db.execute(stmt)

        return result.scalars().first()

    @staticmethod
    async def create(db: AsyncSession, processo: ProcessoCreate) -> ProcessoModel:
        """
        Insert a new process in the database.
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
    async def update(db: AsyncSession, db_processo: ProcessoModel, processo_in: ProcessoUpdate) -> ProcessoModel:
        # Apply only fields present in the request payload.
        update_data = processo_in.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_processo, field, value)
            
        db.add(db_processo)
        await db.commit()
        await db.refresh(db_processo)
        return db_processo

    @staticmethod
    async def save_tese_sugerida(
        db: AsyncSession,
        db_processo: ProcessoModel,
        tese_sugerida: str,
    ) -> ProcessoModel:
        db_processo.tese_sugerida = tese_sugerida
        db.add(db_processo)
        await db.commit()
        await db.refresh(db_processo)
        return db_processo
    
    @staticmethod
    async def delete(db: AsyncSession, db_processo: ProcessoModel) -> None:
        """
        Remove a process from the database.
        """
        await db.delete(db_processo)
        await db.commit()
