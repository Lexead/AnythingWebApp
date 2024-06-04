from abc import ABC, abstractmethod
from uuid import UUID

from anythingwebapp.schemas.file import File


class IFileService(ABC):
    @abstractmethod
    async def save(self, from_path: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get(self, id: UUID) -> File:
        raise NotImplementedError
