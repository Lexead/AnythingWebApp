from pathlib import Path

from pydantic import BaseModel, MySQLDsn, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings


class FastAPISettings(BaseModel):
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "FastAPI application"
    version: str = "0.0.0"


class DatabaseSettings(BaseModel):
    url: PostgresDsn | MySQLDsn
    pool_size: int = 5
    max_overflow: int = 0
    echo: bool = False
    pool_pre_ping: bool = True


class JWTSettings(BaseModel):
    secret_key: SecretStr
    hash_algorithm: str = "bcrypt"
    access_expiration_time: int = 60 * 30
    refresh_expiration_time: int = 60 * 60 * 24 * 7
    issuer: str | None = None
    audience: list[str] | None = None
    access_cookie_key: str = "ACCESS-KEY"
    refresh_cookie_key: str = "REFRESH-KEY"


class AppSettings(BaseSettings):
    """Contains the basic settings of the application."""

    fast_api: FastAPISettings
    database_settings: DatabaseSettings
    jwt_settings: JWTSettings

    allowed_hosts: list[str] = ["*"]

    root_path: Path
    upload_dir: str = "uploads"

    def __init__(self, *args, **kwargs):
        kwargs["fast_api"] = FastAPISettings(_env_file=kwargs["_env_file"])
        kwargs["database_settings"] = DatabaseSettings(_env_file=kwargs["_env_file"])
        kwargs["jwt_settings"] = JWTSettings(_env_file=kwargs["_env_file"])

        super().__init__(*args, **kwargs)
