from sqlalchemy import Column, Integer, String,DateTime, ForeignKeyConstraint, Enum as SqlEnum
from database import Base
from typing import List
import enum

PeriodEnum = enum.Enum(
    'Period',
    {
    '1d': '1d',
    '5d': '5d',
    '1mo': '1mo',
    '3mo': '3mo',
    '6mo': '6mo',
    '1y': '1y',
    '2y': '2y',
    '5y': '5y',
    '10y': '10y',
    'ytd': 'ytd',
    'max': 'max'
    }
)

class WatchlistModel(Base):
    __tablename__ = "watchlist"

    email = Column(String, primary_key=True, nullable=False)
    ticker = Column(String, primary_key=True, nullable=False)
    period = Column(SqlEnum(PeriodEnum),  nullable=True)
    start = Column(DateTime,nullable=True)
    end = Column(DateTime,nullable=True)
    attributes = Column(String, nullable=True)

    @property
    def attributes(self):
        return self.attributes

    @attributes.setter
    def attributes(self, value: List[str]):
        joined_str = ','.join(value)
        self.attributes = joined_str

    __table_args__ = (
        email, ticker
    )