from typing import Optional
from pydantic import BaseModel, constr, EmailStr
from datetime import datetime
from schema.user import UserOut


class PostBase(BaseModel):
    title: str
    description: str
    

class Postout(PostBase):
    created_at: datetime
    

class PostCreate(PostBase):...

class Post(PostBase):
    title: str
    user: UserOut
    class Config:
        orm_mode = True

class PostCreate(PostBase):
    title: str
    description:str
    class Config:
        orm_mode = True



