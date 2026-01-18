from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    DB_HOST: str = "db"
    MYSQL_ROOT_PASSWORD: str
    MYSQL_DATABASE: str = "juridico"
    MODEL_NAME: str = "models/gemini-2.5-flash"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
        
settings = Settings()