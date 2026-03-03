import pytest

payload_base = {
    "numero": "0000001-99.2026.8.26.0001",
    "tipo": "civel",
    "resumo_peticao": "Resumo de teste com mais de vinte caracteres para passar na validacao.",
    "valor_pedido": 15000.50,
    "historico_cliente": "Cliente de teste criado pelo Pytest."
}

@pytest.mark.asyncio
async def test_criar_processo_erro_validacao_pydantic(client):
    # Dados incorretos
    payload_invalido = {
        "numero": "12345", 
        "tipo": "familia", 
        "resumo_peticao": "Curto",
        "valor_pedido": -50.00,
        "historico_cliente": "OK"
    }
    
    response = await client.post("/processos/", json=payload_invalido)

    assert response.status_code == 422
    
    erros = response.json()["detail"]
    assert len(erros) > 0
    assert isinstance(erros, list)

@pytest.mark.asyncio
async def test_criar_processo_duplicado_erro_service(client):
    await client.post("/processos/", json=payload_base)
    
    response_duplicado = await client.post("/processos/", json=payload_base)

    # deve retornar o erro 400 por ser duplicado
    assert response_duplicado.status_code == 400
    
    mensagem_erro = response_duplicado.json()["detail"]
    assert "cadastrado com o número" in mensagem_erro
    
    # deletar processo recém criado
    response_busca = await client.get("/processos/")
    processos = response_busca.json()
    processo_id = next(p["id"] for p in processos if p["numero"] == payload_base["numero"])
    
    await client.delete(f"/processos/{processo_id}")

@pytest.mark.asyncio
async def test_listar_processos_formato_correto(client):
    # Requisicao GET simples para garantir que a rota responde corretamente
    response = await client.get("/processos/")

    assert response.status_code