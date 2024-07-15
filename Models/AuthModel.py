from pydantic import BaseModel
from typing import Optional
from .UserModel import UserModel


class TokenModel(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserInDB(UserModel):
    hashed_password: str
    