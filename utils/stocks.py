from database import db_dependency
from schemas.stocks import StockSearch
import yfinance as yf
import json

def process_tickers(query: StockSearch):
    if len(query.tickers) == 1:
        ticker = yf.Ticker(query.tickers[0])
        trading_history = ticker.history(start=query.start, end=query.end, period=query.period)
        dict_history = json.loads(trading_history.to_json())
        if not ticker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ticker not found"
            )
        else:
            return {
                query.tickers[0]: {
                    "trading_data": dict_history,
                    "info": ticker.info
                }
            }
    else:
        data = yf.download(','.join(query.tickers), start=query.start, end=query.end, period=query.period, group_by="tickers")
        ticker_dict = {}
        if query.fundamentals:
            for ticker in query.tickers:
                ticker_data = yf.Ticker(ticker)
                if ticker_data:
                    ticker_obj = {
                        "trading_data": json.loads(data[ticker].to_json()),
                        "info": ticker_data.info
                    }
                    ticker_dict.update({
                        ticker: ticker_obj
                    })
        return ticker_dict
