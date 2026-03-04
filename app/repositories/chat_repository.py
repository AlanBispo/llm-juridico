from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.mensagem_model import MensagemModel

class ChatRepository:
    
    @staticmethod
    async def buscar_historico(db: AsyncSession, processo_id: int) -> list[MensagemModel]:
        """
        Busca todas as mensagens de um processo, ordenadas pela data de criação.
        """
        stmt = select(MensagemModel).where(MensagemModel.processo_id == processo_id).order_by(MensagemModel.criado_em.asc())
        resultado = await db.execute(stmt)
        return list(resultado.scalars().all())

    @staticmethod
    async def salvar_mensagem(db: AsyncSession, processo_id: int, role: str, conteudo: str) -> MensagemModel:
        """
        Salva uma nova mensagem (do usuário ou da IA) no banco de dados.
        """
        nova_mensagem = MensagemModel(
            processo_id=processo_id,
            role=role,
            conteudo=conteudo
        )
        db.add(nova_mensagem)
        await db.commit()
        await db.refresh(nova_mensagem)
        return nova_mensagem