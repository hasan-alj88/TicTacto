# Authentication setup
from datetime import datetime
from typing import Annotated

import jwt
import logfire
from decouple import config
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlmodel import Session, select

from app.DataModels.AuthData import LoginData, RegisterData
from app.database.DataBaseSetup import db_session
from app.database.models import User, JWTokens

load_dotenv()
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
TIME_ZONE = config('TIME_ZONE', default='UTC')
TOKEN_EXPIRE_MINUTES = config('TOKEN_EXPIRE_MINUTES', default=1440*2, cast=int)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
token_dependency = Annotated [str, Depends(oauth2_scheme)]
db_dependency = Annotated [Session, Depends(db_session)]

async def get_current_username(token: token_dependency):
    with logfire.span("Get current username"):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            username = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            logfire.debug(f"Username: {username}")
            return username
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

username_dependency = Annotated [str, Depends(get_current_username)]

async def get_current_user(username: username_dependency, db: db_dependency):
    with logfire.span("Get current user", username=username):
        statement = select(User).where(User.username == username)
        user = db.exec(statement).one()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user


user_dependency = Annotated [User, Depends(get_current_user)]

async def authenticate_user(payload: LoginData, db: db_dependency)-> User:
    with logfire.span("Authenticate user"):
        username = payload.username
        plain_password = payload.password_plain
        user = select(User).where(User.username == username)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        hashed_password = db.exec(user).one().hashed_password
        if not pwd_context.verify(plain_password, hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect password")
        return db.exec(user).one()

async def jwt_token(payload: LoginData, db: db_dependency)-> str:
    with logfire.span("Authenticate and create JWT token"):
        user = authenticate_user(payload, db)
        username = user.username
        logfire.debug(
            "JWT token created",
            username=username,
            user_id=user.id,
        )
        return jwt.encode({"sub": username}, SECRET_KEY, algorithm=ALGORITHM)

async def authenticate_token(token: token_dependency, db: db_dependency)-> User:
    with logfire.span("Authenticate token"):
        token_record = select(JWTokens).where(JWTokens.access_token == token)
        token_record = db.exec(token_record).one_or_none()
        if token_record is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        if token_record.is_expired:
            raise HTTPException(status_code=401, detail="Token expired")
        username = token_record.username
        user = select(User).where(User.username == username)
        return db.exec(user).one()


async def disable_token(token: token_dependency, db: db_dependency)-> str:
    with logfire.span("Disable token"):
        token_record = select(JWTokens).where(JWTokens.access_token == token)
        token_record = db.exec(token_record).one_or_none()
        if token_record is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        token_record.exp = datetime.now(tz=TIME_ZONE)
        db.add(token_record)
        db.commit()
        db.refresh(token_record)
        return token_record.access_token

async def create_refresh_token(refresh_token: token_dependency, db: db_dependency)-> str:
    with logfire.span("Create refresh token"):
        token_record = select(JWTokens).where(JWTokens.refresh_token == refresh_token)
        token_record = db.exec(token_record).one_or_none()
        if token_record is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        username = await get_current_username(token_record.access_token)
        new_token = jwt.encode({"sub": username}, SECRET_KEY, algorithm=ALGORITHM)
        token_record.access_token = new_token
        token_record.exp = datetime.now(tz=TIME_ZONE) + datetime.timedelta(minutes=TOKEN_EXPIRE_MINUTES)
        db.add(token_record)
        db.commit()
        db.refresh(token_record)
        return token_record.access_token

async def create_new_user(payload: RegisterData, db: db_dependency)-> User:
    with logfire.span("Create new user"):
        user = User(
            username=payload.username,
            hashed_password=pwd_context.hash(payload.password_plain),
            email=payload.email
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user