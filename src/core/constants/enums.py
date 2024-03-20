from src.core.settings import (
    AppSettings,
    DevAppSettings,
    ProdAppSettings,
    TestAppSettings,
)

ENVIRONMENTS: dict[str, type[AppSettings]] = {
    "dev": DevAppSettings,
    "prod": ProdAppSettings,
    "test": TestAppSettings,
}
