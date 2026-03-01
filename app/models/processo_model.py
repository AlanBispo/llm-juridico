import enum
from sqlalchemy import Column, Integer, String, Text, Numeric, Enum
from app.core.database import Base

class TipoProcesso(enum.Enum):
    CIVEL = "civel"
    TRABALHISTA = "trabalhista"
    PENAL = "penal"
    TRIBUTARIO = "tributario"

class ProcessoModel(Base):
    __tablename__ = "processos_judiciais"
    __table_args__ = {'comment': 'Armazena os dados principais dos processos judiciais para análise da IA.'}

    id = Column(Integer, primary_key=True, index=True, comment="Identificador único do processo no sistema.")
    tipo = Column(Enum(TipoProcesso), nullable=False, index=True, comment="Classificação da área do direito.")
    resumo_peticao = Column(Text, nullable=False, comment="Síntese dos fatos e fundamentos da petição inicial.")
    valor_pedido = Column(Numeric(10, 2), nullable=False, comment="Valor da causa ou do pedido principal em reais (R$).")
    historico_cliente = Column(String(255), nullable=False,comment="Histórico ou perfil do cliente para contextualizar a estratégia da IA.")
    numero = Column(String(50), unique=True, index=True, nullable=False, comment="Número do processo no padrão CNJ.")