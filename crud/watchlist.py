from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Annotated
from typing import List, Callable

from database import get_db
from models.watchlist import WatchlistModel
from schemas.watchlist import Watchlist


class WatchlistCRUD:
    def __init__(self, conn: AsyncSession):
        self.db_conn = conn

    @property
    async def db_connection(self) -> AsyncSession:
        return self.db_conn

    async def get_watchlist(self, email: str) -> List[WatchlistModel]:
        watchlist_q = select(WatchlistModel).where(WatchlistModel.email == email)
        watchlist_res = await self.db_conn.execute(watchlist_q)
        watchlist_scalar = watchlist_res.scalar()
        if watchlist_scalar is None:
            return False
        return watchlist_scalar

    async def create_watch_entry(self, watch_data: Watchlist):
        watchlist_q = select(WatchlistModel).where(WatchlistModel.email == email and WatchlistModel.ticker == watch_data.ticker)
        watchlist_res = await self.db_conn.execute(watchlist_q)
        watchlist_scalar = watchlist_res.scalar()
        if watchlist_scalar:
            print("create update method and call")
        else:
            new_watch_entry = WatchlistModel(email=watch_data.email, ticker=watch_data.ticker,
                                             period=watch_data.period, start=watch_data.start,
                                             end=watch_data.end, attributes=watch_data.attributes)
            try:
                self.db_conn.add(new_watch_entry)
                await db.flush()
                await db.refresh(new_user)
                return {
                    "is_created": True,
                    "watch_entry": new_watch_entry
                }
            except Exception as e:
                raise e


def get_watch_repo(db: Annotated[AsyncSession, Depends(get_db)]):
        return WatchlistCRUD(db)
