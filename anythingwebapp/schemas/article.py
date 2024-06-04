from datetime import datetime
from typing import Sequence

from anythingwebapp.schemas.base import BaseIDModel, BaseModel
from anythingwebapp.schemas.file import File


class ViewArticleBlock(BaseModel):
    content: str
    files: Sequence[File]


class ViewArticle(BaseModel):
    title: str
    content: str
    author: str
    blocks: Sequence[ViewArticleBlock]
    created_at: datetime
    updated_at: datetime


class CreateArticle(BaseIDModel):
    title: str
    content: str
    author: str


class FilterArticle(BaseModel):
    title: str | None = None
    author: str | None = None
