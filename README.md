# Juridic - Backend ⚖️

## ⚙️ Projeto em cronstrução 

Motor de inteligência para triagem e análise estratégica de processos judiciais utilizando IA Generativa (**Gemini 2.5**).
### OBS: Utilizando dados completamente fictícios, apenas para fins de estudo.

---

## 🛠️ Tecnologias
* **Python / FastAPI** (Async)
* **MySQL 8.0**
* **Google Gemini 2.5 API**
* **Docker & Docker Compose**

---

## 🚀 Como Executar

1. **Configuração**: Crie um arquivo `.env` na raiz do projeto:
   ```env
   GEMINI_API_KEY=sua_chave_aqui
   MYSQL_ROOT_PASSWORD=sua_senha_root
   MYSQL_DATABASE=juridico
2. **Build e Execução**: Rode o comando docker:
   ```docker
    docker-compose up --build
A API estará disponível em: http://localhost:8000

3. Endpoints Principais
* GET /triagem/{id}: Realiza a análise estratégica do processo e retorna JSON estruturado.
* GET /debug-models: Rota de diagnóstico para listar modelos disponíveis na chave API.

Desenvolvido como objeto de estudos para aprimorar conhecimentos em Python, FastAPI e IA (LLM e IA Generativa).
