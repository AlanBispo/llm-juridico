from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class ChatRequest(BaseModel):
    mensagem: str = Field(
        ..., 
        min_length=2, 
        description="A pergunta ou argumento do advogado para a IA."
    )

# Resposta (texto da IA)
class ChatResponse(BaseModel):
    resposta: str

# Listagem
class MensagemHistoricoResponse(BaseModel):
    id: int
    role: str
    conteudo: str
    criado_em: datetime

    model_config = ConfigDict(from_attributes=True)