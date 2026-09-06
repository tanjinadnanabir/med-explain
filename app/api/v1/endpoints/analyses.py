import uuid

from fastapi import APIRouter, Depends, File, Form, UploadFile, status, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.dependencies import get_db
from app.models.analysis import Analysis
from app.models.user import User
from app.schemas.analysis import AnalysisResponse
from app.services import analysis_service, file_service


router = APIRouter(
    prefix="/analyses",
    tags=["Analyses"],
)


@router.post(
    "",
    response_model=AnalysisResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_analysis_endpoint(
    file: UploadFile = File(...),
    question: str | None = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # image_path = await file_service.save_image(file)
    image_info = await file_service.save_image(file)

    analysis = analysis_service.create_analysis(
        db=db,
        user_id=current_user.id,
        image_path=image_info["path"],
        file_size=image_info["size"],
        image_width=image_info["width"],
        image_height=image_info["height"],
        content_type=image_info["content_type"],
        question=question,
    )

    return analysis


@router.get(
    "",
    response_model=list[AnalysisResponse],
)
def list_analyses(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return analysis_service.get_user_analyses(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{analysis_id}",
    response_model=AnalysisResponse,
)
def get_analysis(
    analysis_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    analysis = analysis_service.get_analysis_by_id(
        db=db,
        analysis_id=analysis_id,
        user_id=current_user.id,
    )

    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found.",
        )

    return analysis
    
    
@router.delete(
    "/{analysis_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_analysis_endpoint(
    analysis_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    analysis = analysis_service.get_analysis_by_id(
        db=db,
        analysis_id=analysis_id,
        user_id=current_user.id,
    )

    if analysis is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found.",
        )

    image_path = analysis.image_path

    analysis_service.delete_analysis(
        db=db,
        analysis=analysis,
    )

    file_service.delete_image(image_path)

    return None