from enum import StrEnum

from sqlalchemy import Enum, Unicode
from sqlalchemy.orm import Mapped, mapped_column

from anythingwebapp.models.base import CustomBaseModel


class PermissionType(StrEnum):
    """The action types."""

    SELECT = "select"
    ADD = "add"
    UPDATE = "update"
    DELETE = "delete"
    ALL = "all"


class Permission(CustomBaseModel):
    """The permission database model."""

    __tablename__ = "actions"

    type: Mapped[PermissionType] = mapped_column(Enum(PermissionType), default=PermissionType.ALL)
    object: Mapped[str] = mapped_column(Unicode(100), nullable=False)
