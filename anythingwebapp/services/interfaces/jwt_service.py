from abc import ABC, abstractmethod
from typing import Any

from fastapi import Response
from pydantic import UUID4

from anythingwebapp.schemas.jwt import Payload


class IJWTService(ABC):
    @abstractmethod
    def get_access_payload(self) -> Payload:
        raise NotImplementedError

    @abstractmethod
    def get_refresh_payload(self) -> Payload:
        raise NotImplementedError

    @abstractmethod
    def refresh_access(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def create_access(self, subject: UUID4) -> None:
        raise NotImplementedError

    @abstractmethod
    def create_refresh(self, subject: UUID4) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_access(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_refresh(self) -> None:
        raise NotImplementedError
