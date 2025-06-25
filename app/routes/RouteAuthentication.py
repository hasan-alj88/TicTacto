import logfire
from decouple import config
from fastapi import APIRouter, status, Depends, HTTPException
from typing import Annotated
import jwt
from jwt.exceptions import JWTException
from passlib.exc import InvalidTokenError
from sqlmodel import Session
from starlette.responses import FileResponse

from app.DataModels.AuthData import TokenData
from app.database.DataBaseSetup import db_session

from pathlib import Path

from app.database.models import User

route_authentication = APIRouter()
