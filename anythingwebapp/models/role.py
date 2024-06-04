from uuid import UUID

from sqlalchemy import ForeignKey, Unicode, UnicodeText
from sqlalchemy.orm import Mapped, mapped_column, relationship

from anythingwebapp.models.base import BaseModel, CustomBaseModel
from anythingwebapp.models.permission import Permission


class Role(CustomBaseModel):
    """The role database model."""

    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(Unicode(50), nullable=False, unique=True, index=True)
    content: Mapped[str | None] = mapped_column(UnicodeText, default=None)

    permissions: Mapped[list[Permission]] = relationship(secondary="role_permissions", backref="roles")


class RolePermission(BaseModel):
    __tablename__ = "role_permissions"

    role_id: Mapped[UUID] = mapped_column(ForeignKey("roles.id"), primary_key=True)
    permission_id: Mapped[UUID] = mapped_column(ForeignKey("permissions.id"), primary_key=True)
