from typing import Any

from pydantic import PostgresDsn, RedisDsn, SecretStr
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    """Base application settings"""

    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "FastAPI application"
    version: str = "0.0.0"

    pg_url: PostgresDsn
    pool_size: int = 2
    max_overflow: int = 0

    redis_url: RedisDsn

    secret_key: SecretStr

    api_prefix: str = "/api"

    allowed_hosts: list[str] = ["*"]

    @property
    def fastapi_kwargs(self) -> dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }

    @property
    def postgres_kwargs(self) -> dict[str, Any]:
        return {"url": self.pg_url.unicode_string(), "pool_size": self.pool_size, "max_overflow": self.max_overflow}
