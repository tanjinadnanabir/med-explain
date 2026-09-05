import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


def create_user(
    db: Session,
    user_data: UserCreate,
) -> User:
    user = User(
        email=user_data.email,
        full_name=user_data.full_name,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def get_user_by_id(
    db: Session,
    user_id: uuid.UUID,
) -> User | None:
    statement = select(User).where(
        User.id == user_id
    )

    return db.scalar(statement)

def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    statement = select(User).where(
        User.email == email
    )

    return db.scalar(statement)

def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 20,
) -> list[User]:
    statement = (
        select(User)
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(statement).all())

def update_user(
    db: Session,
    user: User,
    user_data: UserUpdate,
) -> User:
    update_data = user_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user

def delete_user(
    db: Session,
    user: User,
) -> None:
    db.delete(user)
    db.commit()