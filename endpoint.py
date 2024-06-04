import asyncio
from contextlib import asynccontextmanager
from pathlib import Path, PurePath
from typing import AsyncIterator

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from anythingwebapp.api import router
from anythingwebapp.core.settings import AppSettings, DevAppSettings
from anythingwebapp.providers.database import DatabaseProvider
from anythingwebapp.providers.repository import RepositoryProvider
from anythingwebapp.providers.service import ServiceProvider


class Lifecycle:
    def __init__(self, settings: AppSettings) -> None:
        self.settings = settings

    @asynccontextmanager
    async def __call__(self, app: FastAPI) -> AsyncIterator[None]:
        container = make_async_container(
            DatabaseProvider(),
            RepositoryProvider(),
            ServiceProvider(),
            context={AppSettings: self.settings},
            lock_factory=asyncio.Lock,
        )
        setup_dishka(container, app)
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=self.settings.allowed_hosts)
        app.include_router(router)
        yield
        await container.close()


def get_application() -> FastAPI:
    """Returns the application."""

    cwd = Path.cwd()
    app_settings = DevAppSettings(_env_file=cwd.joinpath("env/dev.env"), root_path=cwd)

    lifecycle = Lifecycle(app_settings)
    app = FastAPI(**app_settings.fast_api, lifespan=lifecycle)

    return app


application = get_application()
