from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, status

from anythingwebapp.models.user import User
from anythingwebapp.services.interfaces import IArticleService, IJWTAuthService

router = APIRouter(prefix="/articles", tags=["auth"], route_class=DishkaRoute)


@router.get("/articles", status_code=status.HTTP_200_OK)
async def articles(article_service: FromDishka[IArticleService], auth_service: FromDishka[IJWTAuthService]):
    _ = await auth_service.get_user()
    return await article_service.all()
