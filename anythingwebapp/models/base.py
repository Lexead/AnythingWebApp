from uuid import UUID, uuid4

from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column


class BaseModel(MappedAsDataclass, DeclarativeBase):
    """The basic database model."""


class CustomBaseModel(BaseModel):
    """The basic database model with column id."""

    id: Mapped[UUID] = mapped_column(primary_key=True, init=False, default=uuid4)

    def _formatted_string(self) -> str:
        string = f"<{self.id}>"

        main_fields = {"name", "title", "username", "email"}

        for main_field in main_fields:
            if hasattr(self, main_field):
                string += f" {getattr(self, main_field)} "

        return string

    def __repr__(self) -> str:
        return self._formatted_string()

    def __str__(self) -> str:
        return self._formatted_string()
