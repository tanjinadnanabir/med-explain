from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.dependencies import get_db


router = APIRouter(
    prefix="/info",
    tags=["Info"],
)


@router.get("")
async def application_info(
    db: Session = Depends(get_db),
):
    result = db.execute(
        text("SELECT 1")
    )

    database_status = (
        "connected"
        if result.scalar() == 1
        else "error"
    )

    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": (
            "development"
            if settings.DEBUG
            else "production"
        ),
        "database": database_status,
    }