from typing import AsyncIterator

from dishka import Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from anythingwebapp.core.settings.app import AppSettings


class DatabaseProvider(Provider):
    settings = from_context(provides=AppSettings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_session_factory(self, settings: AppSettings) -> AsyncIterator[async_sessionmaker[AsyncSession]]:
        async_engine = create_async_engine(**settings.db_settings)
        try:
            yield async_sessionmaker(bind=async_engine, expire_on_commit=False, autoflush=True)
        finally:
            await async_engine.dispose()

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_factory: async_sessionmaker[AsyncSession]) -> AsyncIterator[AsyncSession]:
        async with session_factory() as session, session.begin():
            yield session
