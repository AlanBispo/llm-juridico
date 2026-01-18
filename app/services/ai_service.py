import json
import google.generativeai as genai
from app.core.config import settings

class JuridicoAIEngine:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            model_name=settings.MODEL_NAME,
            generation_config={"response_mime_type": "application/json"}
        )

    async def analisar_acordo_estruturado(self, dados_processo: dict):
        prompt = (
            f"Analise o caso jurídico e retorne um JSON seguindo este esquema: "
            "{'risco': 'Baixo|Médio|Alto', 'valor_sugerido': float, 'justificativa': 'string'}\n\n"
            f"PETIÇÃO: {dados_processo['resumo_peticao']}"
        )
        response = await self.model.generate_content_async(prompt)
        return json.loads(response.text)