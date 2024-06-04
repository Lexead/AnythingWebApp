from datetime import datetime
from enum import StrEnum
from typing import Sequence

from pydantic import UUID4, EmailStr, Field, SecretStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from anythingwebapp.schemas.base import BaseModel


class Header(BaseModel):
    type: str = Field(serialization_alias="typ", default="JWT")
    algorithm: str = Field(serialization_alias="alg")


class Payload(BaseModel):
    jwt_id: UUID4 = Field(serialization_alias="jti")
    subject: UUID4 = Field(serialization_alias="sub")
    expiration_time: int = Field(serialization_alias="exp")
    issuer: str | None = Field(serialization_alias="iss", default=None)
    issued_at: int = Field(serialization_alias="iat")
    not_before: int = Field(serialization_alias="nbf")
    audience: Sequence[str] | None = Field(serialization_alias="aud", default=None)
