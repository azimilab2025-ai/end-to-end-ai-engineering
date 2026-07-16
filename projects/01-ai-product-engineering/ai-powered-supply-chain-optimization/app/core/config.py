import os
from dataclasses import dataclass, field

from dotenv import load_dotenv


load_dotenv()


TRUE_VALUES = {"1", "true", "yes", "on"}
FALSE_VALUES = {"0", "false", "no", "off"}
ALLOWED_ENVIRONMENTS = {
    "development",
    "test",
    "staging",
    "production",
}


def get_str_env(name: str, default: str) -> str:
    return os.getenv(name, default).strip()


def get_bool_env(name: str, default: bool = False) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    normalized_value = value.strip().lower()

    if normalized_value in TRUE_VALUES:
        return True

    if normalized_value in FALSE_VALUES:
        return False

    raise ValueError(
        f"Environment variable {name} must be a boolean value."
    )


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
    app_name: str = field(
        default_factory=lambda: get_str_env(
            "APP_NAME",
            "AI-Powered Supply Chain Optimization API",
        )
    )
    app_version: str = field(
        default_factory=lambda: get_str_env(
            "APP_VERSION",
            "0.1.0",
        )
    )
    environment: str = field(
        default_factory=lambda: get_str_env(
            "ENVIRONMENT",
            "development",
        ).lower()
    )
    debug: bool = field(
        default_factory=lambda: get_bool_env(
            "DEBUG",
            False,
        )
    )

    host: str = field(
        default_factory=lambda: get_str_env(
            "HOST",
            "127.0.0.1",
        )
    )
    port: int = field(
        default_factory=lambda: get_int_env(
            "PORT",
            8000,
        )
    )
    api_prefix: str = field(
        default_factory=lambda: get_str_env(
            "API_PREFIX",
            "/api/v1",
        )
    )

    database_url: str = field(
        default_factory=lambda: get_str_env(
            "DATABASE_URL",
            "sqlite:///./supply_chain.db",
        )
    )

    def __post_init__(self) -> None:
        if not self.app_name:
            raise ValueError("APP_NAME cannot be empty.")

        if not self.app_version:
            raise ValueError("APP_VERSION cannot be empty.")

        if self.environment not in ALLOWED_ENVIRONMENTS:
            allowed = ", ".join(sorted(ALLOWED_ENVIRONMENTS))
            raise ValueError(
                f"ENVIRONMENT must be one of: {allowed}."
            )

        if not self.host:
            raise ValueError("HOST cannot be empty.")

        if not 1 <= self.port <= 65535:
            raise ValueError(
                "PORT must be between 1 and 65535."
            )

        if (
            not self.api_prefix.startswith("/")
            or self.api_prefix.endswith("/")
        ):
            raise ValueError(
                "API_PREFIX must start with '/' and must not end with '/'."
            )

        if not self.database_url:
            raise ValueError("DATABASE_URL cannot be empty.")


settings = Settings()
