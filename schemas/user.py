from pydantic import BaseModel, EmailStr
from typing import Annotated
from fastapi import Body

class UserResponse(BaseModel):
    email: EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

annotated_user_create = Annotated[UserCreate, Body(embed=True)]


