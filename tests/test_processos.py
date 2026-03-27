from unittest.mock import AsyncMock, patch

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

    assert response_duplicado.status_code == 400

    mensagem_erro = response_duplicado.json()["detail"]
    assert "cadastrado com o numero" in mensagem_erro.lower() or "cadastrado com o número" in mensagem_erro

    response_busca = await client.get("/processos/")
    processos = response_busca.json()
    processo_id = next(p["id"] for p in processos if p["numero"] == payload_base["numero"])

    await client.delete(f"/processos/{processo_id}")


@pytest.mark.asyncio
async def test_listar_processos_formato_correto(client):
    response = await client.get("/processos/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
@patch(
    "app.services.processo_service.ProcessoService._gerar_tese_local",
    new_callable=AsyncMock,
)
async def test_gerar_tese_com_provider_local(mock_gerar_tese_local, client):
    mock_gerar_tese_local.return_value = "Tese juridica simulada por modelo local."

    response_proc = await client.post("/processos/", json=payload_base)
    assert response_proc.status_code == 201
    processo_id = response_proc.json()["id"]

    response_tese = await client.post(
        f"/processos/{processo_id}/tese",
        params={"provider": "local", "model_name": "qwen2.5:7b-instruct"},
    )

    assert response_tese.status_code == 200
    assert response_tese.json()["tese_sugerida"] == mock_gerar_tese_local.return_value
    mock_gerar_tese_local.assert_awaited_once()
