from fastapi import APIRouter

from .user import router as user_router
from .authenticate import router as auth_router
from .watchlist import router as watchlist_router
from .stocks import router as stocks_router

api_router = APIRouter()

api_router.include_router(user_router)
api_router.include_router(auth_router)
api_router.include_router(watchlist_router)
api_router.include_router(stocks_router)

