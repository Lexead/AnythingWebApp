from datetime import datetime
from typing import Sequence
from uuid import UUID

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from anythingwebapp.core.settings import AppSettings
from anythingwebapp.models.user import User
from anythingwebapp.repositories.interfaces import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, *, session: AsyncSession, settings: AppSettings) -> None:
        self.session = session
        self.model = User
        self.crypt_context = CryptContext(schemes=[settings.jwt_settings.hash_algorithm], deprecated="auto")

    async def find_by_email(self, email: str) -> User | None:
        query = select(self.model).where(self.model.email.like(email))
        result = await self.session.execute(query)
        return result.scalar()

    async def find_by_username(self, username: str) -> User | None:
        query = select(self.model).where(self.model.username.like(username))
        result = await self.session.execute(query)
        return result.scalar()

    async def find_by_phone_number(self, phone_number: str) -> User | None:
        query = select(self.model).where(self.model.phone_number.like(phone_number))
        result = await self.session.execute(query)
        return result.scalar()

    async def find_by_id(self, id: UUID) -> User | None:
        return await self.session.get(User, id)

    async def all(
        self,
        first_name: str | None = None,
        last_name: str | None = None,
        joined_at: tuple[datetime] | None = None,
        visited_at: tuple[datetime] | None = None,
        limit: int | None = None,
        skip: int | None = None,
    ) -> Sequence[User]:
        query = select(self.model)

        if first_name:
            query = query.where(self.model.first_name.ilike(first_name))

        if last_name:
            query = query.where(self.model.last_name.ilike(last_name))

        if joined_at:
            query = query.where(self.model.joined_at.between(*joined_at))

        if visited_at:
            query = query.where(self.model.visited_at.between(*visited_at))

        if limit:
            query = query.limit(limit)

        if skip:
            query = query.offset(skip)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    def set_password(self, user: User, password: str) -> None:
        user.password_hash = self.crypt_context.hash(password)

    def verify_password(self, user: User, password: str) -> bool:
        return self.crypt_context.verify(password, user.password_hash)
