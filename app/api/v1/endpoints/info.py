from fastapi import APIRouter

from app.core.config import settings


router = APIRouter(
    prefix="/info",
    tags=["Info"],
)


@router.get("")
async def application_info():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": "development" if settings.DEBUG else "production",
    }