from pydantic_settings import SettingsConfigDict

from src.core.constants.paths import ENV_PATH
from src.core.settings.app import AppSettings


class DevAppSettings(AppSettings):
    debug: bool = True
    title: str = "Dev FastAPI application"

    model_config = SettingsConfigDict(env_file=ENV_PATH.joinpath("dev.env"), env_file_encoding="utf-8")
