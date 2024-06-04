from abc import ABC, abstractmethod
from typing import Sequence

from anythingwebapp.schemas.base import BaseFilterModel, BaseIDModel, BaseModel


class IService[ViewModel: BaseModel, CreateModel: BaseIDModel, FilterModel: BaseFilterModel](ABC):
    @abstractmethod
    async def all(self, model: FilterModel) -> Sequence[ViewModel]:
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, model: BaseIDModel) -> ViewModel | None:
        raise NotImplementedError

    @abstractmethod
    async def create(self, model: CreateModel) -> ViewModel:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, model: BaseIDModel) -> None:
        raise NotImplementedError
