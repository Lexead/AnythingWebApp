from datetime import datetime

from pydantic import UUID4, EmailStr, SecretStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from anythingwebapp.schemas.base import BaseModel


class RegistrationModel(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    phone_number: PhoneNumber
    password: str


class LoginModel(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    phone_number: PhoneNumber | None = None
    password: str


class ResetPasswordModel(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    phone_number: PhoneNumber | None = None
    old_password: str
    new_password: str
