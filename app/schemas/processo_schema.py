from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict

from app.models.processo_model import TipoProcesso


class TeseProvider(str, Enum):
    GEMINI = "gemini"
    LOCAL = "local"

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
    tese_sugerida: str | None = None
    model_config = ConfigDict(from_attributes=True)

class ProcessoUpdate(BaseModel):
    numero: Optional[str] = Field(
        None, 
        pattern=r"^\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}$",
        description="Número do processo no formato CNJ"
    )
    tipo: Optional[TipoProcesso] = Field(None, description="Tipo do processo")
    resumo_peticao: Optional[str] = Field(None, min_length=20, description="Resumo dos fatos para análise")
    valor_pedido: Optional[float] = Field(None, gt=0, description="Valor da causa em reais")
    historico_cliente: Optional[str] = Field(None, min_length=5, max_length=255)


class TeseGenerationParams(BaseModel):
    provider: TeseProvider | None = Field(
        default=None,
        description="Provedor de IA para gerar a tese juridica."
    )
    model_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=120,
        description="Nome opcional do modelo a ser usado no provedor selecionado.",
    )
    
    force_regenerate: bool = Field(
        default=False,
        description="Quando true, ignora a tese salva e gera uma nova.",
    )


class TeseGenerationResponse(BaseModel):
    tese_sugerida: str
