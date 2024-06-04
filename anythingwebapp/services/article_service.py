from anythingwebapp.repositories.interfaces import IArticleRepository
from anythingwebapp.schemas.article import ViewArticle
from anythingwebapp.services import Service
from anythingwebapp.services.interfaces import IArticleService


class ArticleService(Service[ViewArticle, ViewArticle, ViewArticle, IArticleRepository], IArticleService):
    pass
