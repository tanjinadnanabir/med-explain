import uuid

from sqlalchemy.orm import Session

from app.models.analysis import Analysis


def create_analysis(
    db: Session,
    user_id: uuid.UUID,
    image_path: str,
    file_size: int,
    image_width: int,
    image_height: int,
    content_type: str,
    question: str | None = None,
    prediction: str | None = None,
    confidence: float | None = None,
    model_version: str | None = None,
) -> Analysis:
    analysis = Analysis(
        user_id=user_id,
        image_path=image_path,
        file_size=file_size,
        image_width=image_width,
        image_height=image_height,
        content_type=content_type,
        question=question,
        prediction=prediction,
        confidence=confidence,
        model_version=model_version,
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return analysis


def get_analysis_by_id(
    db: Session,
    analysis_id: uuid.UUID,
    user_id: uuid.UUID,
) -> Analysis | None:
    return (
        db.query(Analysis)
        .filter(
            Analysis.id == analysis_id,
            Analysis.user_id == user_id,
        )
        .first()
    )


def get_user_analyses(
    db: Session,
    user_id: uuid.UUID,
    skip: int = 0,
    limit: int = 20,
) -> list[Analysis]:
    return (
        db.query(Analysis)
        .filter(Analysis.user_id == user_id)
        .order_by(Analysis.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def delete_analysis(
    db: Session,
    analysis: Analysis,
) -> None:
    db.delete(analysis)
    db.commit()