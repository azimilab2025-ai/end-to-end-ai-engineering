from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "AI Assistant Platform"
    app_env: str = "development"
    app_debug: bool = True
    api_v1_prefix: str = "/api/v1"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_assistant"
    redis_url: str = "redis://localhost:6379/0"
    openai_api_key: str = ""
    jwt_secret_key: str = "replace-with-a-secure-random-value"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
