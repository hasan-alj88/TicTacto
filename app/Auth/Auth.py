# Authentication setup
from typing import Annotated

import jwt
from decouple import config
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlmodel import Session, select, SQLModel

from app.DataModels.AuthData import LoginData
from app.database.DataBaseSetup import db_session
from app.database.models.DBUserAuth import User

load_dotenv()
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
token_dependency = Annotated [str, Depends(oauth2_scheme)]
db_dependency = Annotated [Session, Depends(db_session)]

async def get_current_username(token: token_dependency):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

username_dependency = Annotated [str, Depends(get_current_username)]

async def get_current_user(username: username_dependency, db: db_dependency):
    statement = select(User).where(User.username == username)
    user = db.exec(statement).one()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


user_dependency = Annotated [User, Depends(get_current_user)]

async def jwt_token(payload: LoginData, db: db_dependency)-> str:
    username = payload.username
    plain_password = payload.password_plain

    user = select(User).where(User.username == username)
    hashed_password = db.exec(user).one().hashed_password

    if not pwd_context.verify(plain_password, hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = jwt.encode({"sub": username}, SECRET_KEY, algorithm=ALGORITHM)

    token
    return token