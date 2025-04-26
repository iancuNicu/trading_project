from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from utils.authentication import find_user
from utils.auth_dependencies import verify_token
from crud.watchlist import get_watch_repo, WatchlistCRUD
from typing import Annotated
from database import db_dependency

from schemas.watchlist import Watchlist, WatchlistEntryCreate

router = APIRouter(
    prefix="/watchlist",
    tags=['watchlist'],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_user_watchlist(db: db_dependency,
                             watch_repo: Annotated[WatchlistCRUD, Depends(get_watch_repo)],
                             token: str = Depends(verify_token)):
   user = await find_user(token["sub"], db)
   if not user:
       raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail="Invalid or expired token",
           headers={"WWW-Authenticate": "Bearer"},
       )
   user_watchlist = await watch_repo.get_watchlist(user.email)
   if not user_watchlist:
       return {"watchlist": []}
   else:
       return {"watchlist": user_watchlist}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=WatchlistEntryCreate)
async def create_watchlist_entry(db: db_dependency,
                                 watch_repo: Annotated[WatchlistCRUD, Depends(get_watch_repo)],
                                 watch_create: Watchlist,
                                 token: str = Depends(verify_token)):
    user = await find_user(token["sub"], db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        watch_entry = await watch_repo.create_watch_entry(watch_create)
        return watch_entry
    except Exception as e:
        raise e


