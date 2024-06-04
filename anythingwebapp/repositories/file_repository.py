from anythingwebapp.models import File
from anythingwebapp.repositories.interfaces import IFileRepository
from anythingwebapp.repositories.repository import Repository


class FileRepository(Repository[File], IFileRepository):
    pass
