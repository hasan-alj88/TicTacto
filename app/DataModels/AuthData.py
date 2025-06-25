from datetime import datetime, timedelta

from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()
TOKEN_EXPIRE_MINUTES = int(float(str(1440*2)))

class UserCreateData(BaseModel):
    username: str
    hashed_password: str

class LoginData(BaseModel):
    username: str
    password_plain: str