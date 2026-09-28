"""Application configuration loaded from environment variables."""

from functools import lru_cache
from pathlib import Path
from typing import Annotated, List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BACKEND_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    mongodb_uri: str = Field(default="", alias="MONGODB_URI")
    database_name: str = Field(default="Campus_AI", alias="DATABASE_NAME")
    # Comma-separated in .env — disable JSON decode via NoDecode
    cors_origins: Annotated[List[str], NoDecode] = Field(
        default_factory=lambda: ["http://localhost:5173"],
        alias="CORS_ORIGINS",
    )

    ai_provider: str = Field(default="ollama", alias="AI_PROVIDER")
    ollama_base_url: str = Field(
        default="http://localhost:11434",
        alias="OLLAMA_BASE_URL",
    )
    ollama_model: str = Field(default="llama3.2", alias="OLLAMA_MODEL")
    ai_api_key: str = Field(default="", alias="AI_API_KEY")
    ai_model: str = Field(default="", alias="AI_MODEL")
    ai_timeout_seconds: int = Field(default=60, alias="AI_TIMEOUT_SECONDS")

    knowledge_base_dir: Path = Field(
        default=BACKEND_DIR.parent / "data" / "daviet",
        alias="KNOWLEDGE_BASE_DIR",
    )
    error_audit_collection: str = Field(
        default="error_audit",
        alias="ERROR_AUDIT_COLLECTION",
    )
    chat_history_collection: str = Field(
        default="chat_history",
        alias="CHAT_HISTORY_COLLECTION",
    )
    knowledge_collection: str = Field(
        default="knowledge_items",
        alias="KNOWLEDGE_COLLECTION",
    )
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: object) -> List[str]:
        if value is None or value == "":
            return ["http://localhost:5173"]
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        if isinstance(value, str):
            return [part.strip() for part in value.split(",") if part.strip()]
        return ["http://localhost:5173"]

    @field_validator("knowledge_base_dir", mode="before")
    @classmethod
    def resolve_knowledge_dir(cls, value: object) -> Path:
        if value is None or value == "":
            return BACKEND_DIR.parent / "data" / "daviet"
        path = Path(str(value))
        if not path.is_absolute():
            path = (BACKEND_DIR / path).resolve()
        return path


@lru_cache
def get_settings() -> Settings:
    return Settings()
