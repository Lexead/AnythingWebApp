from anythingwebapp.models import File
from anythingwebapp.repositories.interfaces.repository import IRepository


class IFileRepository(IRepository[File]):
    pass
