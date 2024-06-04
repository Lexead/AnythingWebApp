from fastapi import APIRouter

from anythingwebapp.api.routers.auth import router as auth_router

router = APIRouter()
router.include_router(auth_router)
