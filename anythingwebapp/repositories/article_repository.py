from anythingwebapp.models import Article
from anythingwebapp.repositories.interfaces import IFileRepository
from anythingwebapp.repositories.repository import Repository


class ArticleRepository(Repository[Article], IFileRepository):
    pass
