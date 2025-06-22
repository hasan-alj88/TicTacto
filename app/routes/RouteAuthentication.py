from fastapi import APIRouter, status, Depends, HTTPException
from typing import Annotated
from sqlmodel import Session
from app.database.models import (
    UserRead,
    UserCreate,
)
from app.database.DataBaseSetup import get_session
from app.database.crud import create_user

route_authentication = APIRouter()


@route_authentication.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED)
def register_user(
    user: UserCreate,
    session: Annotated[Session, Depends(get_session)]
):
    """
    Register a new user - public endpoint
    """
    try:
        db_user = create_user(session, user)
        return db_user
    except HTTPException:
        raise