import jwt
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Annotated, Union

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

from models.user import UserModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def find_user(email: str, db: AsyncSession):
    user_q = select(UserModel).where(UserModel.email == email)
    user_res = await db.execute(user_q)
    user_scalar = user_res.scalar()
    if user_scalar is None:
        return False
    return user_scalar

def create_hash_pass(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def authenticate_user(db: AsyncSession, email: str, password: str):
    user_q = select(UserModel).where(UserModel.email == email)
    user_res = await db.execute(user_q)
    user_scalar = user_res.scalar()
    if not user_scalar or not verify_password(password, user_scalar.password):
        return False
    return user_scalar

def create_access_token(data: dict):
    to_encode = data.copy()
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    expire = datetime.now(timezone.utc) + access_token_expires
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    access_token_expires = timedelta(minutes=60 * 24 * 7) # 7 days
    expire = datetime.now(timezone.utc) + access_token_expires
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt




