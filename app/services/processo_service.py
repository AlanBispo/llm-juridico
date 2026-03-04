from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.processo_schema import ProcessoCreate, ProcessoUpdate
from app.repositories.processo_repository import ProcessoRepository

from google import genai
from app.core.config import settings

MODEL_NAME = settings.MODEL_NAME
class ProcessoService:
    
    @staticmethod
    async def criar_processo(db: AsyncSession, processo_in: ProcessoCreate):
        processo_existente = await ProcessoRepository.buscar_por_numero(db, processo_in.numero)
        
        if processo_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Já existe um processo cadastrado com o número {processo_in.numero}."
            )
        
        processo_criado = await ProcessoRepository.create(db=db, processo=processo_in)
        
        return processo_criado
    
    @staticmethod
    async def listar_processos(db: AsyncSession, skip: int = 0, limit: int = 100):
        return await ProcessoRepository.get_all(db=db, skip=skip, limit=limit)

    @staticmethod
    async def obter_processo_por_id(db: AsyncSession, processo_id: int):
        processo = await ProcessoRepository.get_by_id(db=db, processo_id=processo_id)
        
        if not processo:
            raise HTTPException(status_code=404, detail="Processo não encontrado.")
            
        return processo
    
    @staticmethod
    async def atualizar_processo(db: AsyncSession, processo_id: int, processo_in: ProcessoUpdate):
        # Verifica se o processo existe
        db_processo = await ProcessoRepository.get_by_id(db=db, processo_id=processo_id)
        if not db_processo:
            raise HTTPException(status_code=404, detail="Processo não encontrado para atualização.")
        
        # Verifica número CNJ duplicado.
        if processo_in.numero and processo_in.numero != db_processo.numero:
            processo_existente = await ProcessoRepository.get_by_numero(db=db, numero=processo_in.numero)
            if processo_existente:
                raise HTTPException(
                    status_code=400, 
                    detail="Já existe outro processo cadastrado com este novo número CNJ."
                )

        return await ProcessoRepository.update(db=db, db_processo=db_processo, processo_in=processo_in)
    
    @staticmethod
    async def deletar_processo(db: AsyncSession, processo_id: int):
        # Verifica se o processo existe
        db_processo = await ProcessoRepository.get_by_id(db=db, processo_id=processo_id)
        
        if not db_processo:
            raise HTTPException(status_code=404, detail="Processo não encontrado para exclusão.")
        
        # Chama o repositório para deletar do banco
        await ProcessoRepository.delete(db=db, db_processo=db_processo)

    @staticmethod
    async def gerar_tese_estrategica(db: AsyncSession, processo_id: int):
        # busca o processo
        processo = await ProcessoRepository.get_by_id(db, processo_id)
        if not processo:
            raise HTTPException(status_code=404, detail="Processo não encontrado.")

        # verifica se a tese já foi gerada antes para economizar recursos
        if processo.tese_sugerida:
            return processo

        # Prompt com o contexto do processo
        prompt = f"""
        Você é um advogado especialista e estrategista.
        Analise os dados abaixo e formule uma tese jurídica sólida e direta ao ponto para o caso.
        
        Tipo da Ação: {processo.tipo.value}
        Valor do Pedido: R$ {processo.valor_pedido}
        Histórico do Cliente: {processo.historico_cliente}
        Resumo dos Fatos: {processo.resumo_peticao}
        
        Forneça apenas a tese jurídica sugerida, sem introduções ou saudações.
        """

        try:
            client = genai.Client(api_key=settings.GEMINI_API_KEY)
            
            resposta = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )
            tese_gerada = resposta.text
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao conectar com a IA: {str(e)}")

        processo.tese_sugerida = tese_gerada
        await db.commit()
        await db.refresh(processo)

        return processo