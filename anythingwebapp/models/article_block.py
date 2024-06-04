from datetime import UTC, datetime
from uuid import UUID

from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import ImageType
from slugify import slugify
from sqlalchemy import DateTime, ForeignKey, Unicode, UnicodeText
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from anythingwebapp.models.base import BaseModel, CustomBaseModel
from anythingwebapp.models.file import File
from anythingwebapp.models.user import User


class ArticleBlock(CustomBaseModel):
    __tablename__ = "article_blocks"

    content: Mapped[str] = mapped_column(UnicodeText)
    article_id: Mapped[UUID] = mapped_column(ForeignKey("articles.id", ondelete="cascade"))

    files: Mapped[list[File]] = relationship(secondary="article_block_files", backref="article_blocks", lazy="selectin")


class ArticleBlockFile(BaseModel):
    __tablename__ = "article_block_files"

    article_block_id: Mapped[UUID] = mapped_column(ForeignKey("article_blocks.id"), primary_key=True)
    file_id: Mapped[UUID] = mapped_column(ForeignKey("files.id"), primary_key=True)
