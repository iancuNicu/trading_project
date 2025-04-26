from pydantic import BaseModel
from models.watchlist import PeriodEnum
from datetime import datetime
from typing import Literal, List

period_val_tuple = tuple(member.name for member in PeriodEnum)

class TradingData(BaseModel):
    period: Literal[period_val_tuple] = None
    start: datetime
    end: datetime

class StockSearch(BaseModel):
    tickers: List[str]
    fundamentals: bool
    period: Literal[period_val_tuple] = None
    start: datetime = None
    end: datetime = None
