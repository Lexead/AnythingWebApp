from pydantic_settings import SettingsConfigDict

from app.core.constants.paths import ENV_PATH
from app.core.settings.app import AppSettings


class TestAppSettings(AppSettings):
    debug: bool = True
    title: str = "Test FastAPI application"

    model_config = SettingsConfigDict(env_file=ENV_PATH.joinpath("test.env"), env_file_encoding="utf-8")
