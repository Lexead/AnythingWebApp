from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Unicode, UnicodeText
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from anythingwebapp.models.base import BaseModel, CustomBaseModel
from anythingwebapp.models.user import User


class File(CustomBaseModel):
    __tablename__ = "files"

    name: Mapped[str] = mapped_column(Unicode(100))
    mime_type: Mapped[str] = mapped_column(Unicode(50))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), init=False, default_factory=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), init=False, nullable=True, onupdate=datetime.now(UTC)
    )
    author_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="cascade"))

    author: Mapped[User] = relationship(backref="files", lazy="joined", innerjoin=True)
