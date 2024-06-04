from anythingwebapp.models import Article
from anythingwebapp.repositories.interfaces.repository import IRepository


class IArticleRepository(IRepository[Article]):
    pass
