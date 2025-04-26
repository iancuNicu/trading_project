from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status
from typing import Annotated

from database import db_dependency
from schemas.stocks import StockSearch
from utils.auth_dependencies import verify_token
from utils.authentication import find_user
from utils.stocks import process_tickers

router = APIRouter(
    prefix="/stocks",
    tags=['stocks'],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_tickers_info(db: db_dependency,
                         ticker_query: Annotated[StockSearch, Query()],
                         token: str = Depends(verify_token)):
    user = await find_user(token["sub"], db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return process_tickers(ticker_query)

