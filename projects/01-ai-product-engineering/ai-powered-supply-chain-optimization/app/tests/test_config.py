import pytest

from app.core.config import Settings, get_bool_env


ENVIRONMENT_VARIABLES = (
    "APP_NAME",
    "APP_VERSION",
    "ENVIRONMENT",
    "DEBUG",
    "HOST",
    "PORT",
    "API_PREFIX",
    "DATABASE_URL",
)


def clear_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    for variable_name in ENVIRONMENT_VARIABLES:
        monkeypatch.delenv(variable_name, raising=False)


def test_default_settings(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clear_environment(monkeypatch)

    settings = Settings()

    assert settings.app_name == (
        "AI-Powered Supply Chain Optimization API"
    )
    assert settings.app_version == "0.1.0"
    assert settings.environment == "development"
    assert settings.debug is False
    assert settings.host == "127.0.0.1"
    assert settings.port == 8000
    assert settings.api_prefix == "/api/v1"
    assert settings.database_url == (
        "sqlite:///./supply_chain.db"
    )


def test_settings_read_environment_values(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("APP_NAME", "Supply Chain Production API")
    monkeypatch.setenv("APP_VERSION", "1.0.0")
    monkeypatch.setenv("ENVIRONMENT", "PRODUCTION")
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("HOST", "0.0.0.0")
    monkeypatch.setenv("PORT", "9000")
    monkeypatch.setenv("API_PREFIX", "/api/v2")
    monkeypatch.setenv(
        "DATABASE_URL",
        "sqlite:///./production.db",
    )

    settings = Settings()

    assert settings.app_name == "Supply Chain Production API"
    assert settings.app_version == "1.0.0"
    assert settings.environment == "production"
    assert settings.debug is True
    assert settings.host == "0.0.0.0"
    assert settings.port == 9000
    assert settings.api_prefix == "/api/v2"
    assert settings.database_url == (
        "sqlite:///./production.db"
    )


def test_invalid_boolean_environment_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DEBUG", "sometimes")

    with pytest.raises(
        ValueError,
        match="DEBUG must be a boolean value",
    ):
        get_bool_env("DEBUG")


@pytest.mark.parametrize("invalid_port", ["0", "65536"])
def test_invalid_port_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
    invalid_port: str,
) -> None:
    monkeypatch.setenv("PORT", invalid_port)

    with pytest.raises(
        ValueError,
        match="PORT must be between 1 and 65535",
    ):
        Settings()


def test_invalid_environment_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ENVIRONMENT", "unknown")

    with pytest.raises(
        ValueError,
        match="ENVIRONMENT must be one of",
    ):
        Settings()


@pytest.mark.parametrize(
    "invalid_prefix",
    ["api/v1", "/api/v1/"],
)
def test_invalid_api_prefix_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
    invalid_prefix: str,
) -> None:
    monkeypatch.setenv("API_PREFIX", invalid_prefix)

    with pytest.raises(
        ValueError,
        match="API_PREFIX must start",
    ):
        Settings()
