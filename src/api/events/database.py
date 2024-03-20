from typing import Callable

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine

from src.core.settings import AppSettings


def on_startup(app: FastAPI, settings: AppSettings) -> Callable:
    async def on_connect() -> None:
        async_engine = create_async_engine(**settings.postgres_kwargs)
        app.state.engine = async_engine

    return on_connect


def on_shutdown(app: FastAPI) -> Callable:
    async def on_disconnect() -> None:
        await app.state.engine.dispose()

    return on_disconnect
