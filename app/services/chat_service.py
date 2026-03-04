from google import genai
from google.genai import types
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.core.config import settings
from app.repositories.chat_repository import ChatRepository
from app.repositories.processo_repository import ProcessoRepository

MODEL_NAME = settings.MODEL_NAME

class ChatService:
    
    INSTRUCOES_ESPECIALISTA = """
    Você é um Advogado Sênior Especialista em Direito Civil, focado em Direito do Consumidor e Responsabilidade Civil.
    Seu papel é atuar como um consultor estratégico para outros advogados.
    Seja técnico, cite jurisprudências do STJ aplicáveis e fundamente-se no Código de Defesa do Consumidor (CDC) ou Código Civil.
    Seja direto e objetivo. Não responda a perguntas que fujam do escopo jurídico.
    """

    @staticmethod
    async def enviar_mensagem(db: AsyncSession, processo_id: int, mensagem_usuario: str) -> str:
        processo = await ProcessoRepository.get_by_id(db, processo_id)
        if not processo:
            raise HTTPException(status_code=404, detail="Processo não encontrado.")

        historico_db = await ChatRepository.buscar_historico(db, processo_id)
        
        historico_gemini = []
        for msg in historico_db:
            historico_gemini.append(
                types.Content(
                    role=msg.role,
                    parts=[types.Part.from_text(text=msg.conteudo)]
                )
            )

        # Inicialização do novo Client
        client = genai.Client(api_key=settings.GEMINI_API_KEY)

        # Configuração das instruções de sistema
        config = types.GenerateContentConfig(
            system_instruction=ChatService.INSTRUCOES_ESPECIALISTA,
        )

        try:
            # Criação do chat passando o histórico e as configurações
            chat = client.chats.create(
                model= MODEL_NAME,
                history=historico_gemini,
                config=config
            )
            
            resposta_ia = chat.send_message(mensagem_usuario)
            texto_resposta = resposta_ia.text
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao processar resposta da IA: {str(e)}")

        await ChatRepository.salvar_mensagem(db, processo_id, role="user", conteudo=mensagem_usuario)
        await ChatRepository.salvar_mensagem(db, processo_id, role="model", conteudo=texto_resposta)

        return texto_resposta