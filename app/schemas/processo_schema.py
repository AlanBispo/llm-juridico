from pydantic import BaseModel, Field, ConfigDict
from app.models.processo_model import TipoProcesso

class ProcessoCreate(BaseModel):
    # Regex para validar exatamente o formato do CNJ
    numero: str = Field(
        ..., 
        pattern=r"^\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}$",
        description="Número do processo no formato CNJ",
        examples=["1234567-89.2023.8.26.0001"]
    )
    tipo: TipoProcesso = Field(..., description="Tipo do processo (civel, trabalhista, etc)")
    resumo_peticao: str = Field(..., min_length=20, description="Resumo dos fatos para análise")
    # O valor não pode ser negativo nem zero
    valor_pedido: float = Field(..., gt=0, description="Valor da causa em reais")
    historico_cliente: str = Field(..., min_length=5, max_length=255)

class ProcessoResponse(ProcessoCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)