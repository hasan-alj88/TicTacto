from datetime import datetime, timedelta
from typing import Annotated

import jwt
from fastapi import APIRouter, HTTPException, status, Form


from app.Auth import (
    db_dependency,
    token_dependency,
    user_dependency,
    jwt_token,
    disable_token,
    create_refresh_token,
    TOKEN_EXPIRE_MINUTES,
    TIME_ZONE,
    SECRET_KEY,
    ALGORITHM, create_new_user,
)
from app.DataModels.AuthData import LoginData, RegisterData
from app.database.models import JWTokens

# Create router for authentication endpoints
route_authentication = APIRouter(prefix="/auth", tags=["authentication"])


# @route_authentication.post("/register")
# async def register(payload, db: db_dependency):
#     """
#     Register a new user
#     """
#     try:
#         # Create a new user instance
#         user = User(
#             username=payload.username,
#             hashed_password=pwd_context.hash(payload.password_plain),
#             email=payload.email
#         )

@route_authentication.post("/login")
async def login(payload: LoginData, db: db_dependency):
    """
    Authenticate user and return access and refresh tokens
    """
    try:
        # Generate access token
        access_token = await jwt_token(payload, db)

        # Generate refresh token (longer expiration)
        refresh_token = jwt.encode(
            {"sub": payload.username, "type": "refresh"},
            SECRET_KEY,
            algorithm=ALGORITHM
        )

        # Store tokens in the database
        token_record = JWTokens(
            username=payload.username,
            access_token=access_token,
            refresh_token=refresh_token,
            exp=datetime.now(tz=TIME_ZONE) + timedelta(minutes=TOKEN_EXPIRE_MINUTES),
            refresh_exp=datetime.now(tz=TIME_ZONE) + timedelta(days=1)
        )

        db.add(token_record)
        db.commit()
        db.refresh(token_record)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": TOKEN_EXPIRE_MINUTES * 60  # seconds
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication failed."
                   f"\nException: {e.__class__.__name__}: {e}",
        )


@route_authentication.get("/logout")
async def logout(token: token_dependency, db: db_dependency):
    """
    Logout user by disabling their current token
    Protected endpoint - requires valid access token
    """
    try:
        disabled_token = await disable_token(token, db)
        return {
            "message": "Successfully logged out",
            "disabled_token": disabled_token
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )


@route_authentication.post("/token_refresh")
async def token_refresh(refresh_token: str, db: db_dependency):
    """
    Refresh access token using refresh token
    Protected endpoint - requires valid refresh token
    """
    try:
        new_access_token = await create_refresh_token(refresh_token, db)
        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": TOKEN_EXPIRE_MINUTES * 60
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )


@route_authentication.get("/profile")
async def get_user_profile(user: user_dependency):
    """
    Get current authenticated user profile
    Protected endpoint - requires valid access token
    """
    return {
        "id": user.id,
        "username": user.username,
        "email": getattr(user, 'email', None),  # If email field exists
        # Add other non-sensitive user fields as needed
    }


# Alternative endpoint that returns JSON (for API clients)
@route_authentication.post("/api/auth/register")
async def register_user_api(
        email: Annotated[str, Form()],
        username: Annotated[str, Form()],
        full_name: Annotated[str, Form()],
        password: Annotated[str, Form()],
        confirm_password: Annotated[str, Form()],
        db: db_dependency
):
    """
    Handle user registration and return JSON response
    """
    try:
        if password != confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match"
            )

        register_data = RegisterData(
            username=username,
            password=password,
            email=email,
            full_name=full_name,
            confirm_password=confirm_password
        )

        new_user = await create_new_user(register_data, db)

        return {
            "message": "User registered successfully",
            "user_id": new_user.id,
            "username": new_user.username,
            "email": new_user.email
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )