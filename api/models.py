import re
import uuid

from fastapi import HTTPException
from pydantic import BaseModel, validator, EmailStr

class TunedModel(BaseModel):

    # convert event non dict obj to json
    class Config:
        orm_mode = True


class UserShow(TunedModel):
    user_id: uuid.UUID
    email: EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str

