from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GEMINI_API_KEY: str | None = None
    AI_PROVIDER: str = "local"
    GEMINI_MODEL_NAME: str = "gemini-2.5-flash"
    GEMINI_FALLBACK_TO_LOCAL: bool = True
    LOCAL_LLM_BASE_URL: str = "http://ollama:11434"
    LOCAL_LLM_MODEL: str = "qwen2.5:3b-instruct"
    LOCAL_LLM_TIMEOUT: int = 120
    
    # Configurações do PostgreSQL
    DB_HOST: str = "db"
    DB_PORT: str = "5432"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = "juridico"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # String de conexão para o SQLAlchemy
    @property
    def DATABASE_URL(self) -> str:
        # driver assíncrono asyncpg
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.POSTGRES_DB}"

settings = Settings()
