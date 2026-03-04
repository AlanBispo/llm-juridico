from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class MensagemModel(Base):
    __tablename__ = "mensagens_chat"
    __table_args__ = {'comment': 'Armazena o histórico de conversas com a IA especialista.'}

    id = Column(Integer, primary_key=True, index=True)
    processo_id = Column(Integer, ForeignKey("processos_judiciais.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(50), nullable=False)
    conteudo = Column(Text, nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())