from dishka import Provider, Scope, from_context, provide
from fastapi import Request, Response

from anythingwebapp.core.settings import AppSettings
from anythingwebapp.repositories.interfaces import IFileRepository, IUserRepository
from anythingwebapp.services import FileService, JWTAuthService, JWTService
from anythingwebapp.services.interfaces import (
    IFileService,
    IJWTAuthService,
    IJWTService,
)


class ServiceProvider(Provider):
    settings = from_context(provides=AppSettings, scope=Scope.APP)
    request = from_context(provides=Request, scope=Scope.REQUEST)
    response = from_context(provides=Response, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    def jwt_service(self, request: Request, response: Response, settings: AppSettings) -> IJWTService:
        return JWTService(request=request, response=response, settings=settings)

    @provide(scope=Scope.REQUEST)
    def jwt_auth_service(
        self, user_repository: IUserRepository, jwt_service: IJWTService, settings: AppSettings
    ) -> IJWTAuthService:
        return JWTAuthService(user_repository=user_repository, jwt_service=jwt_service, settings=settings)

    @provide(scope=Scope.REQUEST)
    def file_service(
        self, file_repository: IFileRepository, jwt_auth_service: IJWTAuthService, settings: AppSettings
    ) -> IFileService:
        return FileService(file_repository=file_repository, jwt_auth_service=jwt_auth_service, settings=settings)
