from pydantic import UUID4
from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict


class BaseModel(_BaseModel):
    model_config = ConfigDict(from_attributes=True)


class BaseIDModel(BaseModel):
    id: UUID4 | None = None


class BaseFilterModel(BaseModel):
    limit: int | None = None
    skip: int | None = None
