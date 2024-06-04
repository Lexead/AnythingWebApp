from dataclasses import dataclass, field
from typing import Any, Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from anythingwebapp.models.base import CustomBaseModel
from anythingwebapp.repositories.interfaces.repository import IRepository


class Repository[Model: CustomBaseModel](IRepository[Model]):
    def __init__(self, *, session: AsyncSession, model: type[Model] = Model) -> None:
        self.session = session
        self.model = model

    async def all(self, limit: int | None = None, skip: int | None = None) -> Sequence[Model]:
        query = select(self.model)

        if limit:
            query = query.limit(limit)

        if skip:
            query = query.offset(skip)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def find_by_id(self, id: UUID) -> Model | None:
        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        return result.scalar()

    async def create(self, **kwargs: Any) -> Model:
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def delete_by_id(self, id: UUID) -> None:
        instance = await self.session.get(self.model, id)
        await self.session.delete(instance)
