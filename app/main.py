import os
import asyncio
import aiomysql
import google.generativeai as genai
from fastapi import FastAPI, HTTPException

# --- CONFIGURAÇÃO DE AMBIENTE (DOCKER) ---
API_KEY = os.getenv("GEMINI_API_KEY")
DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = "root"
DB_PASS = os.getenv("MYSQL_ROOT_PASSWORD")
DB_NAME = os.getenv("MYSQL_DATABASE", "juridico")

# versão 2.5 Flash do gemini
MODEL_NAME = 'models/gemini-2.5-flash'

if not API_KEY:
    print("ERRO: Variável GEMINI_API_KEY não configurada no .env")
else:
    genai.configure(api_key=API_KEY)

app = FastAPI(
    title="Judiciario API",
    description="Plataforma de triagem estratégica de processos judiciais usando LLM",
    version="2.0.0"
)

# Banco
class LegalDatabase:
    """Responsável exclusiva pela conexão e consultas ao MySQL."""
    def __init__(self):
        self.config = {
            'host': DB_HOST,
            'user': DB_USER,
            'password': DB_PASS,
            'db': DB_NAME,
            'autocommit': True
        }

    async def obter_processo(self, processo_id: int):
        """Busca dados brutos do processo de forma assíncrona."""
        conn = None
        try:
            conn = await aiomysql.connect(**self.config)
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                query = "SELECT resumo_peticao, valor_pedido, historico_cliente FROM processos_judiciais WHERE id = %s"
                await cursor.execute(query, (processo_id,))
                return await cursor.fetchone()
        except Exception as e:
            print(f" Erro na consulta ao MySQL: {e}")
            raise e
        finally:
            if conn:
                conn.close()

# IA?
class LegalAIEngine:
    """Define a lógica de Prompt e a comunicação com a LLM."""
    def __init__(self):
        self.model = genai.GenerativeModel(MODEL_NAME)

    async def analisar_viabilidade_acordo(self, dados_processo: dict):
        """Envia o contexto jurídico e retorna análise."""
        prompt = (
            f"Você é um mediador sênior do sistema judiciário. Analise este caso:\n\n"
            f"PETIÇÃO: {dados_processo['resumo_peticao']}\n"
            f"VALOR DA CAUSA: R$ {dados_processo['valor_pedido']}\n"
            f"PERFIL DO AUTOR: {dados_processo['historico_cliente']}\n\n"
            "Gere uma resposta estruturada com: \n"
            "1. Risco de perda (Baixo/Médio/Alto)\n"
            "2. Sugestão de valor para acordo\n"
            "3. Argumento para negociação."
        )
        
        try:
            # Chamada assíncrona para a API do Google
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            print(f"Erro na API do Gemini: {e}")
            raise e


class JudiciarioService:
    def __init__(self):
        self.db = LegalDatabase()
        self.ai = LegalAIEngine()

    async def executar_triagem(self, processo_id: int):
        # 1. Recupera dados do banco
        dados = await self.db.obter_processo(processo_id)
        if not dados:
            return None
        
        # 2. Processa via IA
        analise = await self.ai.analisar_viabilidade_acordo(dados)
        
        return {
            "id_processo": processo_id,
            "valor_original": dados['valor_pedido'],
            "modelo_ia": MODEL_NAME,
            "analise_estrategica": analise
        }

service = JudiciarioService()

@app.get("/")
async def health_check():
    """Rota de verificação de status do sistema."""
    return {
        "status": "online",
        "engine": MODEL_NAME,
        "database_host": DB_HOST
    }

@app.get("/debug-models")
async def listar_modelos():
    """Rota utilitária para verificar permissões da API Key."""
    try:
        modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        return {"modelos_disponiveis": modelos}
    except Exception as e:
        return {"erro": str(e)}

@app.get("/triagem/{processo_id}")
async def triagem_processo(processo_id: int):
    """Rota principal para obter a triagem"""
    try:
        resultado = await service.executar_triagem(processo_id)
        
        if not resultado:
            raise HTTPException(status_code=404, detail="Processo não encontrado no banco de dados.")
            
        return resultado
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no processamento: {str(e)}")