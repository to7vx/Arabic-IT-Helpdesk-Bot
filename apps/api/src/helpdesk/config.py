"""Application settings loaded from environment + .env.

Single source of truth for every runtime knob. See ``.env.example`` at the
repo root for documentation of each field. Settings are cached so
``get_settings()`` is cheap to call from anywhere.
"""

from __future__ import annotations

from enum import StrEnum
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppEnv(StrEnum):
    development = "development"
    staging = "staging"
    production = "production"


class LLMProvider(StrEnum):
    disabled = "disabled"
    claude = "claude"
    jais = "jais"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env", "../../.env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Core ------------------------------------------------------------------
    app_env: AppEnv = AppEnv.development
    app_name: str = "arabic-helpdesk"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    secret_key: SecretStr = SecretStr("change-me-please-32-bytes-minimum-length")
    allowed_origins: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def _split_csv(cls, value: object) -> object:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    # Database --------------------------------------------------------------
    database_url: str = (
        "postgresql+asyncpg://helpdesk:helpdesk@localhost:5432/helpdesk"
    )
    db_pool_size: int = 10
    db_pool_max_overflow: int = 20
    db_echo: bool = False

    # Redis / Celery --------------------------------------------------------
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    # Object storage --------------------------------------------------------
    s3_endpoint: str = "http://localhost:9000"
    s3_region: str = "us-east-1"
    s3_bucket: str = "helpdesk-attachments"
    s3_access_key: SecretStr = SecretStr("minioadmin")
    s3_secret_key: SecretStr = SecretStr("minioadmin")
    s3_force_path_style: bool = True

    # Vector store ----------------------------------------------------------
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: SecretStr | None = None

    # Multi-tenancy ---------------------------------------------------------
    multi_tenant: bool = False
    default_org_slug: str = "default"

    # Auth ------------------------------------------------------------------
    jwt_algorithm: Literal["RS256", "HS256"] = "RS256"
    jwt_private_key_path: Path = Path("./secrets/jwt-private.pem")
    jwt_public_key_path: Path = Path("./secrets/jwt-public.pem")
    jwt_access_ttl_min: int = 15
    jwt_refresh_ttl_days: int = 14

    oauth_google_client_id: str = ""
    oauth_google_client_secret: SecretStr = SecretStr("")
    oauth_microsoft_client_id: str = ""
    oauth_microsoft_client_secret: SecretStr = SecretStr("")
    oauth_microsoft_tenant: str = "common"

    saml_metadata_url: str = ""
    saml_entity_id: str = ""

    # NLP / LLM -------------------------------------------------------------
    llm_provider: LLMProvider = LLMProvider.disabled

    anthropic_api_key: SecretStr = SecretStr("")
    anthropic_model: str = "claude-opus-4-7"
    anthropic_prompt_cache: bool = True

    jais_base_url: str = "http://localhost:11434"
    jais_model: str = "jais-30b-chat"

    embedding_model: str = "BAAI/bge-m3"
    reranker_model: str = "BAAI/bge-reranker-v2-m3"

    nlp_category_min_confidence: float = 0.55
    nlp_urgency_threshold: float = 0.75

    # Email ingest ----------------------------------------------------------
    email_ingest_enabled: bool = False
    imap_host: str = ""
    imap_user: str = ""
    imap_password: SecretStr = SecretStr("")
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: SecretStr = SecretStr("")
    smtp_from: str = "helpdesk@example.com"

    # Integrations ----------------------------------------------------------
    slack_bot_token: SecretStr = SecretStr("")
    slack_signing_secret: SecretStr = SecretStr("")
    teams_app_id: str = ""
    teams_app_password: SecretStr = SecretStr("")
    whatsapp_business_token: SecretStr = SecretStr("")
    whatsapp_phone_number_id: str = ""

    # Observability ---------------------------------------------------------
    otel_exporter_otlp_endpoint: str = "http://localhost:4318"
    otel_service_name: str = "helpdesk-api"
    prometheus_metrics_port: int = 9100

    # Derived ---------------------------------------------------------------
    @property
    def is_production(self) -> bool:
        return self.app_env is AppEnv.production


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
