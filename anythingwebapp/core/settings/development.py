from pydantic_settings import SettingsConfigDict

from anythingwebapp.core.settings.app import AppSettings


class DevAppSettings(AppSettings):
    debug: bool = True
    title: str = "Dev FastAPI application"
