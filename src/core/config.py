from src.core.constants.enums import ENVIRONMENTS
from src.core.settings import AppSettings


def get_app_settings(app_type: str) -> AppSettings:
    return ENVIRONMENTS[app_type]()
