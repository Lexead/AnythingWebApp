from pathlib import Path, PurePath
from uuid import UUID

import aiofiles
import magic

from anythingwebapp.core.settings import AppSettings
from anythingwebapp.repositories.interfaces import IFileRepository
from anythingwebapp.schemas.file import File
from anythingwebapp.services.interfaces import IFileService, IJWTAuthService


class FileService(IFileService):
    def __init__(
        self, *, file_repository: IFileRepository, jwt_auth_service: IJWTAuthService, settings: AppSettings
    ) -> None:
        self.file_repository = file_repository
        self.jwt_auth_service = jwt_auth_service
        self.settings = settings

    async def _read(self, file_path: str) -> bytes:
        async with aiofiles.open(file_path, "rb") as file:
            content = await file.read()
        return content

    async def _write(self, file_path: str, content: bytes) -> None:
        async with aiofiles.open(file_path, "wb") as file:
            await file.write(content)

    async def save(self, from_path: str) -> None:
        download_path = PurePath(from_path)
        content = await self._read(from_path)

        user = await self.jwt_auth_service.get_user()

        upload_path = Path(self.settings.root_path, self.settings.upload_dir, str(user.id), download_path.name)
        upload_path.mkdir(parents=True, exist_ok=True)
        await self._write(str(upload_path), content)

        mime_type = magic.from_file(download_path.name, mime=True)
        await self.file_repository.create(name=download_path.name, mime_type=mime_type, author_id=user.id)

    async def get(self, id: UUID) -> File:
        file = await self.file_repository.find_by_id(id)

        download_path = Path(self.settings.root_path, self.settings.upload_dir, str(file.author_id), file.name)
        download_path.mkdir(parents=True, exist_ok=True)
        data = await self._read(download_path)

        return File(data=data, mime_type=file.mime_type)
