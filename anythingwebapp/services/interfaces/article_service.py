from anythingwebapp.schemas.article import ViewArticle
from anythingwebapp.services.interfaces import IService


class IArticleService(IService[ViewArticle, ViewArticle, ViewArticle]):
    pass
