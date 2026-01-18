from app.db.database import JuridicoDatabase
from app.services.ai_service import JuridicoAIEngine

class JuridicoService:
    def __init__(self):
        self.db = JuridicoDatabase()
        self.ai = JuridicoAIEngine()

    async def executar_fluxo_triagem(self, processo_id: int):
        dados = await self.db.obter_processo(processo_id)
        if not dados:
            return None
        
        analise = await self.ai.analisar_acordo_estruturado(dados)
        return {"processo_id": processo_id, "analise": analise}