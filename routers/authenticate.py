from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from database import db_dependency

from utils.authentication import (authenticate_user, create_access_token,
                                  find_user, create_hash_pass, create_refresh_token)
from utils.auth_dependencies import (verify_ref_token)
from schemas.user import annotated_user_create, UserResponse
from models.user import UserModel

router = APIRouter(
    prefix="/authenticate",
    tags=['authenticate'],
    responses={404: {"description": "Not found"}},
)

@router.post("/login")
async def login(user: annotated_user_create, db: db_dependency):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid user or login data",
        headers={"WWW-Authenticate": "Bearer"},
    )
    db_user = await authenticate_user(db, user.email, user.password)
    if not db_user:
        raise credentials_exception

    token = create_access_token(data={"sub": user.email})
    ref_token = create_refresh_token(data={"sub": user.email})
    user = UserResponse(email=user.email)

    return {"access_token": token, "refresh_token": ref_token,"user": user}

@router.post("/signup",  status_code=status.HTTP_201_CREATED)
async def signup(user: annotated_user_create,  db: db_dependency):
    user_exists_exception = HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="User already exists"
    )
    db_user = await find_user(user.email, db)
    if db_user:
        raise user_exists_exception
    else:
        hash_pass = create_hash_pass(user.password)
        new_user = UserModel(email=user.email, password=hash_pass)
        db.add(new_user)
        await db.flush()
        await db.refresh(new_user)
        token = create_access_token(data={"sub": user.email})
        ref_token = create_refresh_token(data={"sub": user.email})
        user = UserResponse(email=user.email)
        return {"access_token": token, "refresh_token": ref_token, "user": user}

@router.post("/refresh-token")
async def refresh_token(db: db_dependency, ref_token = Depends(verify_ref_token)):
    db_user = await find_user(ref_token["sub"], db)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        token = create_access_token(data={"sub": db_user.email})
        return {"access_token": token}


