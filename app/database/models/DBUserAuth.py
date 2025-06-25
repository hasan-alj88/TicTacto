from datetime import datetime, timedelta
from enum import IntEnum
from typing import Optional

from decouple import config
from dotenv import load_dotenv
from sqlmodel import SQLModel, Field

load_dotenv()
TIME_ZONE = config('TIME_ZONE', default='UTC')
time_zone = datetime.now(tz=TIME_ZONE).astimezone().tzinfo
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
    created_at: datetime = Field(default_factory=lambda :datetime.now(tz=time_zone))

class JWTokens(SQLModel, table=True):
    __tablename__ = "jwt_tokens"
    id: Optional[int] = Field(default=None, primary_key=True)
    access_token: str
    refresh_token: str
    iat: datetime = Field(default_factory=lambda :datetime.now(tz=time_zone))
    exp: datetime = Field(default_factory=lambda :datetime.now(tz=time_zone)+timedelta(minutes=TOKEN_EXPIRE_MINUTES))