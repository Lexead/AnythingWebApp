from abc import ABC, abstractmethod
from datetime import datetime
from typing import Sequence
from uuid import UUID

from anythingwebapp.models import User


class IUserRepository(ABC):
    @abstractmethod
    async def find_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_username(self, username: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_phone_number(self, phone_number: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, id: UUID) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def all(
        self,
        first_name: str | None = None,
        last_name: str | None = None,
        joined_at: tuple[datetime] | None = None,
        visited_at: tuple[datetime] | None = None,
        limit: int | None = None,
        skip: int | None = None,
    ) -> Sequence[User]:
        raise NotImplementedError

    @abstractmethod
    async def create(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def set_password(self, user: User, password: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def verify_password(self, user: User, password: str) -> bool:
        raise NotImplementedError
