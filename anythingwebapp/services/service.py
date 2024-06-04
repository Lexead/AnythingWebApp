from typing import Any, Sequence, override

from pydantic import TypeAdapter

from anythingwebapp.repositories.interfaces.repository import IRepository
from anythingwebapp.schemas.base import BaseFilterModel, BaseIDModel, BaseModel
from anythingwebapp.services.interfaces.service import IService


class Service[
    ViewModel: BaseModel,
    CreateModel: BaseIDModel,
    FilterModel: BaseFilterModel,
    Repository: IRepository[BaseModel],
](IService[ViewModel, CreateModel, FilterModel]):
    def __init__(
        self,
        *,
        repository: Repository,
        view_model: type[ViewModel] = ViewModel,
        create_model: type[CreateModel] = CreateModel,
        filter_model: type[FilterModel] = FilterModel,
    ) -> None:
        self.repository = repository
        self.view_model = view_model
        self.create_model = create_model
        self.filter_model = filter_model

    async def all(self, model: FilterModel) -> Sequence[ViewModel]:
        orm_models = await self.repository.all(**model.model_dump(exclude_unset=True))
        adapter = TypeAdapter(list[self.view_model])
        return adapter.validate_python(orm_models)

    async def find_by_id(self, model: BaseIDModel) -> ViewModel | None:
        orm_model = await self.repository.find_by_id(model.id)
        return self.view_model.model_validate(orm_model)

    async def create(self, model: CreateModel) -> ViewModel:
        orm_model = await self.repository.create(**model.model_dump(exclude_unset=True))
        return self.view_model.model_validate(orm_model)

    async def delete_by_id(self, model: BaseIDModel) -> None:
        await self.repository.delete_by_id(model.id)
