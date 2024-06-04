from datetime import UTC, datetime
from typing import Sequence
from uuid import uuid4

import jwt
from fastapi import HTTPException, Request, Response, status
from pydantic import UUID4

from anythingwebapp.core.settings import AppSettings
from anythingwebapp.schemas.jwt import Header, Payload
from anythingwebapp.services.interfaces.jwt_service import IJWTService


class JWTService(IJWTService):
    def __init__(self, *, request: Request, response: Response, settings: AppSettings) -> None:
        self.request = request
        self.response = response
        self.jwt_settings = settings.jwt_settings

    def _create_token(
        self,
        subject: UUID4,
        expiration_time: int,
    ) -> str:
        payload = Payload(
            jwt_id=uuid4(),
            subject=subject,
            expiration_time=expiration_time,
            issuer=self.jwt_settings.issuer,
            issued_at=int(datetime.now(UTC).timestamp()),
            not_before=int(datetime.now(UTC).timestamp()),
            audience=self.jwt_settings.audience,
        )

        header = Header(algorithm=self.jwt_settings.hash_algorithm)

        return jwt.encode(
            payload.model_dump(),
            self.jwt_settings.secret_key.get_secret_value(),
            self.jwt_settings.hash_algorithm,
            header.model_dump(),
        )

    def _read_token(
        self,
        encoded_token: str,
    ) -> Payload:
        try:
            unverified_header = Header.model_validate(jwt.get_unverified_header(encoded_token))
            payload = jwt.decode(
                encoded_token,
                self.jwt_settings.secret_key.get_secret_value(),
                algorithms=[unverified_header.algorithm],
                issuer=self.jwt_settings.issuer,
                audience=self.jwt_settings.audience,
            )
            return Payload.model_validate(payload)
        except Exception as err:
            raise HTTPException(status.HTTP_403_FORBIDDEN, str(err))

    def _get_payload(self, key: str) -> Payload:
        token = self.request.cookies.get(key)

        if token is None:
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"The token {key} wasn't found.")

        return self._read_token(token)

    def get_access_payload(self) -> Payload:
        return self._get_payload(self.jwt_settings.access_cookie_key)

    def get_refresh_payload(self) -> Payload:
        return self._get_payload(self.jwt_settings.refresh_cookie_key)

    def refresh_access(self) -> None:
        payload = self.get_refresh_payload()
        self.create_access(payload.subject)

    def create_access(self, subject: UUID4) -> None:
        access_token = self._create_token(subject, self.jwt_settings.access_expiration_time)

        self.response.set_cookie(
            self.jwt_settings.access_cookie_key,
            access_token,
            self.jwt_settings.access_expiration_time,
            self.jwt_settings.access_expiration_time,
            httponly=True,
        )

    def create_refresh(self, subject: UUID4) -> None:
        refresh_token = self._create_token(subject, self.jwt_settings.refresh_expiration_time)

        self.response.set_cookie(
            self.jwt_settings.refresh_cookie_key,
            refresh_token,
            self.jwt_settings.refresh_expiration_time,
            self.jwt_settings.refresh_expiration_time,
            httponly=True,
        )

    def delete_access_cookie(self) -> None:
        self.response.delete_cookie(self.jwt_settings.access_cookie_key, httponly=True)

    def delete_refresh_cookie(self) -> None:
        self.response.delete_cookie(self.jwt_settings.refresh_cookie_key, httponly=True)
