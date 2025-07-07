from datetime import datetime, timedelta
from enum import IntEnum
from typing import Optional

from decouple import config
from dotenv import load_dotenv
from sqlmodel import SQLModel, Field, Column, Boolean, func, Computed, DateTime

from Utils.Time import parse_timezone_string

load_dotenv()
TIME_ZONE = config('TIME_ZONE', default='UTC')
time_zone = parse_timezone_string(TIME_ZONE)
TOKEN_EXPIRE_MINUTES = config('TOKEN_EXPIRE_MINUTES', default=1440*2, cast=int)

class UserRole(IntEnum):
    ADMIN = 1
    USER = 2

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    role: UserRole = Field(default=UserRole.USER)
    hashed_password: str
    created_at: datetime = Field(
        sa_column=Column(
            DateTime,
            server_default=func.datetime('now')
        )
    )

class JWTokens(SQLModel, table=True):
    __tablename__ = "jwt_tokens"
    id: Optional[int] = Field(default=None, primary_key=True)
    access_token: str
    refresh_token: str
    iat: datetime = Field(
        sa_column=Column(
            DateTime,
            server_default=func.datetime('now')
        )
    )
    exp: datetime = Field(
        sa_column=Column(
            DateTime,
            server_default=func.datetime('now', f'+{TOKEN_EXPIRE_MINUTES} minutes')
        )
    )

    is_expired: bool = Field(
        sa_column=Column(
            Boolean,
            Computed("datetime('now') > exp")
        )
    )