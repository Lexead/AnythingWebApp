from app.core.constants.enums import ENVIRONMENTS
from app.core.settings import AppSettings


def get_app_settings(app_type: str) -> AppSettings:
    return ENVIRONMENTS[app_type]()
