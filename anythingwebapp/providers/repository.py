from dishka import Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import AsyncSession

from anythingwebapp.core.settings import AppSettings
from anythingwebapp.repositories import (
    ArticleRepository,
    FileRepository,
    UserRepository,
)
from anythingwebapp.repositories.interfaces import (
    IArticleRepository,
    IFileRepository,
    IUserRepository,
)


class RepositoryProvider(Provider):
    settings = from_context(provides=AppSettings, scope=Scope.APP)

    @provide(scope=Scope.REQUEST)
    def article_repository(self, session: AsyncSession) -> IArticleRepository:
        return ArticleRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def file_repository(self, session: AsyncSession) -> IFileRepository:
        return FileRepository(session=session)

    @provide(scope=Scope.REQUEST)
    def user_repository(self, session: AsyncSession, settings: AppSettings) -> IUserRepository:
        return UserRepository(session=session, settings=settings)
