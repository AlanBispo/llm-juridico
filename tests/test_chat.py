import pytest
from unittest.mock import patch, MagicMock

payload_processo_chat = {
    "numero": "0005555-44.2026.8.05.0001",
    "tipo": "civel",
    "resumo_peticao": "Teste de chat para atraso de voo.",
    "valor_pedido": 10000.00,
    "historico_cliente": "Cliente perdeu conexão."
}

@pytest.mark.asyncio
@patch("app.services.chat_service.genai.Client")
async def test_fluxo_completo_chat(mock_client_class, client):
    mock_resposta = MagicMock()
    mock_resposta.text = "Segundo o CDC, a companhia aérea responde objetivamente pelo atraso."
    
    # Simula o objeto chat
    mock_chat_instance = MagicMock()
    mock_chat_instance.send_message.return_value = mock_resposta
    
    # Simula o cliente e a sua propriedade 'chats'
    mock_client_instance = MagicMock()
    mock_client_instance.chats.create.return_value = mock_chat_instance
    
    mock_client_class.return_value = mock_client_instance

    
    response_proc = await client.post("/processos/", json=payload_processo_chat)
    assert response_proc.status_code == 201
    processo_id = response_proc.json()["id"]

    payload_chat = {"mensagem": "Qual a responsabilidade da companhia aérea?"}
    response_chat = await client.post(f"/processos/{processo_id}/chat", json=payload_chat)
    
    assert response_chat.status_code == 200
    assert response_chat.json()["resposta"] == mock_resposta.text

    # Verifica a chamada no novo formato
    mock_chat_instance.send_message.assert_called_once_with(payload_chat["mensagem"])

    response_historico = await client.get(f"/processos/{processo_id}/chat")
    assert response_historico.status_code == 200
    historico = response_historico.json()
    
    assert len(historico) == 2
    assert historico[0]["role"] == "user"
    assert historico[1]["role"] == "model"
    assert historico[1]["conteudo"] == mock_resposta.text

    await client.delete(f"/processos/{processo_id}")