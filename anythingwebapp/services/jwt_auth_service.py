from fastapi import HTTPException, status
from pydantic import UUID4

from anythingwebapp.models.user import User
from anythingwebapp.repositories.interfaces.user_repository import IUserRepository
from anythingwebapp.schemas.auth import (
    LoginModel,
    RegistrationModel,
    ResetPasswordModel,
)
from anythingwebapp.services.interfaces.jwt_auth_service import IJWTAuthService
from anythingwebapp.services.interfaces.jwt_service import IJWTService


class JWTAuthService(IJWTAuthService):
    def __init__(self, *, user_repository: IUserRepository, jwt_service: IJWTService) -> None:
        self.user_repository = user_repository
        self.jwt_service = jwt_service

    def _create_token_pair(self, subject: UUID4) -> None:
        self.jwt_service.create_access(subject)
        self.jwt_service.create_refresh(subject)

    def _delete_token_pair(self) -> None:
        self.jwt_service.delete_access()
        self.jwt_service.create_refresh()

    async def login(self, model: LoginModel) -> None:
        user = None

        if not model.username is None and user is None:
            user = await self.user_repository.find_by_username(model.username)

        if not model.email is None and user is None:
            user = await self.user_repository.find_by_email(model.email)

        if not model.phone_number is None and user is None:
            user = await self.user_repository.find_by_phone_number(model.phone_number)

        if user is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "The user wasn't found.")

        if self.user_repository.verify_password(user, model.password):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "The user wasn't verified.")

        self._create_token_pair(user.id)

    async def register(self, model: RegistrationModel) -> None:
        user = User(**model.model_dump())
        self.user_repository.set_password(user, model.password)
        user = await self.user_repository.create(user)

        self._create_token_pair(user.id)

    async def reset_password(self, model: ResetPasswordModel) -> None:
        user = await self.user_repository.find_by_email(model.email)

        if not user:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "The user wan't found.")

        if self.user_repository.verify_password(user, model.old_password):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "The user wasn't verified.")

        self.user_repository.set_password(user, model.new_password)
        user = await self.user_repository.create(user)

        self.jwt_service.create_access(user.id)

    async def refresh(self) -> None:
        self.jwt_service.refresh_access()

    async def logout(self) -> None:
        self._delete_token_pair()

    async def get_user(self) -> User:
        payload = self.jwt_service.get_access_payload()

        user = await self.user_repository.find_by_id(payload.subject)

        if user is None:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "The user wasn't found.")

        return user
