from pydantic_settings import SettingsConfigDict

from app.core.constants.paths import ENV_PATH
from app.core.settings.app import AppSettings


class ProdAppSettings(AppSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH.joinpath("prod.env"), env_file_encoding="utf-8")
