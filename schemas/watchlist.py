from pydantic import BaseModel, EmailStr
from models.watchlist import PeriodEnum
from datetime import datetime
from typing import List, Optional

class Watchlist(BaseModel):
    email: EmailStr
    ticker: str
    period: Optional[PeriodEnum] = None
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    attributes: Optional[List[str]] = None

class WatchlistEntryCreate(BaseModel):
    is_created: bool
    watch_entry: Watchlist



