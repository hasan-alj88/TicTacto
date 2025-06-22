from fastapi import HTTPException, status
from sqlmodel import Session, select
from app.database.models import User, UserCreate, UserUpdate
from app.database.auth import get_password_hash, get_user_by_username
from typing import Optional


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """Get user by email"""
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return session.get(User, user_id)


def create_user(session: Session, user: UserCreate) -> User:
    """Create a new user"""
    # Check if user already exists
    if get_user_by_email(session, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    if get_user_by_username(session, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    # Create user with hashed password
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_password,
        is_active=user.is_active
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def update_user(session: Session, user_id: int, user_update: UserUpdate) -> User:
    """Update an existing user"""
    db_user = get_user_by_id(session, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update only provided fields
    user_data = user_update.model_dump(exclude_unset=True)
    for field, value in user_data.items():
        setattr(db_user, field, value)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_all_users(session: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """Get all users with pagination"""
    statement = select(User).offset(skip).limit(limit)
    return session.exec(statement).all()