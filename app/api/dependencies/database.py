from asyncio import current_task
from typing import AsyncGenerator

from fastapi import Depends, Request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
)


def _get_async_scoped_session(request: Request) -> async_scoped_session[AsyncSession]:
    async_engine: AsyncEngine = request.app.state.engine
    session_factory = async_sessionmaker(bind=async_engine, expire_on_commit=False, class_=AsyncSession)
    scoped_session = async_scoped_session(session_factory=session_factory, scopefunc=current_task)
    return scoped_session


async def get_session(
    scoped_session: async_scoped_session[AsyncSession] = Depends(_get_async_scoped_session),
) -> AsyncGenerator[AsyncSession, None]:
    async with scoped_session() as session:
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.commit()
            await scoped_session.remove()
