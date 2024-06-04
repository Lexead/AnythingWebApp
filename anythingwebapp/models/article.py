from datetime import UTC, datetime
from uuid import UUID

from slugify import slugify
from sqlalchemy import DateTime, ForeignKey, Unicode, UnicodeText
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from anythingwebapp.models.article_block import ArticleBlock
from anythingwebapp.models.base import BaseModel, CustomBaseModel
from anythingwebapp.models.user import User


class Article(CustomBaseModel):
    """The post database model."""

    __tablename__ = "articles"

    title: Mapped[str] = mapped_column(Unicode(50), unique=True, index=True)
    slug: Mapped[str] = mapped_column(
        Unicode(50), unique=True, index=True, init=False, onupdate=slugify(title), default=slugify(title)
    )
    content: Mapped[str] = mapped_column(UnicodeText)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), init=False, default_factory=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), init=False, nullable=True, onupdate=datetime.now(UTC)
    )
    author_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="cascade"))

    author: Mapped[User] = relationship(backref="articles", lazy="joined", innerjoin=True)
    blocks: Mapped[list[ArticleBlock]] = relationship(backref="articles", lazy="selectin")

    # @validates("title")
    # def update_slug(self, key, title):
    #     self.slug = slugify(title)
    #     return title
