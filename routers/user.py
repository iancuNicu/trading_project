from fastapi import APIRouter, Depends, HTTPException
from database import db_dependency
from starlette import status

from utils.authentication import find_user
from utils.auth_dependencies import verify_token
from schemas.user import UserResponse

router = APIRouter(
    prefix="/user",
    tags=['user'],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_user(db: db_dependency, token: str = Depends(verify_token)):
   user = await find_user(token["sub"], db)
   if not user:
       raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail="Invalid or expired token",
           headers={"WWW-Authenticate": "Bearer"},
       )
   return UserResponse(email=user.email)



