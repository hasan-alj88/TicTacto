import logfire
import secrets
from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlmodel import Session, select
from app.database.models import User
from app.database.DataBaseSetup import get_session

# Built-in FastAPI Basic Authentication
security = HTTPBasic()


def get_password_hash(password: str) -> str:
    """Simple password hashing - in production use proper hashing like bcrypt"""
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return get_password_hash(plain_password) == hashed_password


def get_user_by_username(session: Session, username: str) -> Optional[User]:
    """Get user from database by username"""
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()


def authenticate_user(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
        session: Annotated[Session, Depends(get_session)]
) -> User:
    """
    Authenticate user using FastAPI's built-in HTTPBasic authentication
    """
    with logfire.span("authenticate_user", usename=credentials.username):
        # Get user from database
        user = get_user_by_username(session, credentials.username)

        # Verify credentials using secrets.compare_digest for security
        if not user or not secrets.compare_digest(
                credentials.username, user.username
        ) or not verify_password(credentials.password, user.hashed_password):
            logfire.error("Authentication failed")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )

        if not user.is_active:
            logfire.error("Inactive user")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        return user


