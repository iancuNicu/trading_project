from sqlalchemy import Column, Integer, String
from database import Base

class UserModel(Base):
    __tablename__ = "users"

    email=Column(String, primary_key=True, nullable=False)
    password=Column(String, nullable=False)
