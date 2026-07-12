import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


def get_bool_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def get_int_env(name: str, default: int) -> int:
    value = os.getenv(name)

    if value is None:
        return default

    try:
        return int(value)
    except ValueError as exc:
        raise ValueError(
            f"Environment variable {name} must be an integer."
        ) from exc


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv(
        "APP_NAME",
        "AI-Powered Supply Chain Optimization API",
    )
    app_version: str = os.getenv("APP_VERSION", "0.1.0")
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = get_bool_env("DEBUG", False)

    host: str = os.getenv("HOST", "127.0.0.1")
    port: int = get_int_env("PORT", 8000)
    api_prefix: str = os.getenv("API_PREFIX", "/api/v1")

    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./supply_chain.db",
    )


settings = Settings()