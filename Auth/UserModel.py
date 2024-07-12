from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class UserModel(BaseModel):
    id:Optional[UUID] = None
    email:str
    token:Optional[str] = None
    password:str
    first_name:Optional[str] = None
    last_name:Optional[str] = None
    rsvp:str