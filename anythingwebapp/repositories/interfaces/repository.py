from abc import ABC, abstractmethod
from typing import Any, Sequence
from uuid import UUID

from anythingwebapp.models.base import CustomBaseModel  # pylint: disable=W0611


class IRepository[Model: CustomBaseModel](ABC):
    @abstractmethod
    async def all(self, limit: int | None = None, skip: int | None = None) -> Sequence[Model]:  # pylint: disable=E0602
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, id: UUID) -> Model | None:  # pylint: disable=E0602,W0622
        raise NotImplementedError

    @abstractmethod
    async def create(self, **kwargs: Any) -> Model:  # pylint: disable=E0602
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, id: UUID) -> None:  # pylint: disable=W0622
        raise NotImplementedError
