from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Unicode, UnicodeText
from sqlalchemy.orm import Mapped, mapped_column, relationship

from anythingwebapp.models.base import CustomBaseModel


class Location(CustomBaseModel):
    """The user database model."""

    __tablename__ = "locations"

    name: Mapped[str] = mapped_column(Unicode(100), nullable=False)
    tz_offset: Mapped[int]
    lang_code: Mapped[str] = mapped_column(Unicode(10), nullable=False)
