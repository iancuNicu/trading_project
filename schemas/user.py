from pydantic import BaseModel

class User(BaseModel):
    email: str

class UserCreate(BaseModel):
    email: str


