from anythingwebapp.core.settings.app import AppSettings


class TestAppSettings(AppSettings):
    debug: bool = True
    title: str = "Test FastAPI application"
