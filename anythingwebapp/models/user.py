from datetime import UTC, datetime, timedelta, timezone
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Unicode, UnicodeText
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from anythingwebapp.models.base import BaseModel, CustomBaseModel
from anythingwebapp.models.location import Location
from anythingwebapp.models.permission import Permission
from anythingwebapp.models.role import Role


class User(CustomBaseModel):
    """The user database model."""

    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(Unicode(50), nullable=False)
    last_name: Mapped[str | None] = mapped_column(Unicode(50), nullable=True)
    username: Mapped[str] = mapped_column(Unicode(20), nullable=False, unique=True, index=True)
    email: Mapped[str] = mapped_column(Unicode(50), nullable=False, unique=True, index=True)
    phone_number: Mapped[str] = mapped_column(Unicode(50), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(UnicodeText)
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), init=False, default_factory=lambda: datetime.now(UTC)
    )
    visited_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), init=False, nullable=True)
    location_id: Mapped[UUID] = mapped_column(ForeignKey("locations.id"))

    location: Mapped[Location] = relationship(backref="users", lazy="joined", innerjoin=True)
    roles: Mapped[list[Role]] = relationship(secondary="user_roles", backref="users", lazy="selectin")
    permissions: Mapped[list[Permission]] = relationship(secondary="user_permissions", backref="users", lazy="selectin")

    @hybrid_property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name or ''}"

    @hybrid_property
    def joined_at_with_tz(self) -> datetime:
        return self.joined_at.replace(tzinfo=timezone(timedelta(seconds=self.location.tz_offset)))

    @hybrid_property
    def visited_at_with_tz(self) -> datetime:
        return self.visited_at.replace(tzinfo=timezone(timedelta(seconds=self.location.tz_offset)))


class UserPermission(BaseModel):
    __tablename__ = "user_permissions"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    permission_id: Mapped[UUID] = mapped_column(ForeignKey("permissions.id"), primary_key=True)


class UserRole(BaseModel):
    __tablename__ = "user_roles"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    role_id: Mapped[UUID] = mapped_column(ForeignKey("roles.id"), primary_key=True)
