from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class UserModel(BaseModel):
    id:Optional[UUID] = None
    email:str
    password: str
    token:Optional[str] = None
    first_name:Optional[str] = None
    last_name:Optional[str] = None
    rsvp:str