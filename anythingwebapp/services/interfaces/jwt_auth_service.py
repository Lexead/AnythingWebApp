from abc import ABC, abstractmethod

from anythingwebapp.models.user import User
from anythingwebapp.schemas.auth import (
    LoginModel,
    RegistrationModel,
    ResetPasswordModel,
)


class IJWTAuthService(ABC):
    @abstractmethod
    async def login(self, model: LoginModel) -> None:
        raise NotImplementedError

    @abstractmethod
    async def register(self, model: RegistrationModel) -> None:
        raise NotImplementedError

    @abstractmethod
    async def reset_password(self, model: ResetPasswordModel) -> None:
        raise NotImplementedError

    @abstractmethod
    async def refresh(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def logout(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_user(self) -> User:
        raise NotImplementedError
