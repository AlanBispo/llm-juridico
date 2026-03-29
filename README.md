# Juridic - Backend

Motor de inteligência para triagem e análise estratégica de processos judiciais utilizando IA generativa.

## Tecnologias
* Python / FastAPI
* PostgreSQL 15
* Google Gemini
* Ollama
* Docker Compose

## Como executar

1. Crie o arquivo `.env` na raiz:

```env
POSTGRES_PASSWORD=root
POSTGRES_DB=juridico
POSTGRES_USER=postgres
AI_PROVIDER=local
LOCAL_LLM_MODEL=qwen2.5:3b-instruct
```

2. Suba a aplicação, banco e Ollama:

```bash
docker compose up --build -d
```

3. Baixe o modelo no container do Ollama:

```bash
docker compose exec ollama ollama pull qwen2.5:3b-instruct
```

4. A API ficará disponível em `http://localhost:8000`.

## Conexão com IA local

O backend agora usa por padrão `http://ollama:11434`, que funciona quando `app` e `ollama` estão na mesma rede do Docker Compose.

Se você preferir continuar rodando o Ollama fora do Docker, por exemplo no WSL, defina no `.env`:

```env
LOCAL_LLM_BASE_URL=http://host.docker.internal:11434
```

O serviço `app` já foi configurado com `host.docker.internal` via `host-gateway`, o que evita depender de IP fixo.

## Endpoints principais
* `GET /triagem/{id}`: gera a tese estratégica do processo.
* `GET /debug-models`: rota de diagnóstico para os modelos remotos.
