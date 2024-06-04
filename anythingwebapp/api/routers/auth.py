from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status

from anythingwebapp.schemas.auth import (
    LoginModel,
    RegistrationModel,
    ResetPasswordModel,
)
from anythingwebapp.services.interfaces import IJWTAuthService

router = APIRouter(prefix="/auth", tags=["auth"], route_class=DishkaRoute)


@router.post("/register", status_code=status.HTTP_200_OK)
async def register(model: RegistrationModel, auth_service: FromDishka[IJWTAuthService]):
    await auth_service.register(model)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(model: LoginModel, auth_service: FromDishka[IJWTAuthService]):
    await auth_service.login(model)


@router.post("/reset_password", status_code=status.HTTP_200_OK)
async def reset_password(model: ResetPasswordModel, auth_service: FromDishka[IJWTAuthService]):
    await auth_service.reset_password(model)


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh(auth_service: FromDishka[IJWTAuthService]):
    await auth_service.refresh()
