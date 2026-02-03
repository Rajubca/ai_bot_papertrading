from fastapi import APIRouter, Query
import random

router = APIRouter()


@router.get("/quote")
def get_quote(symbol: str = Query(...)):
    """
    Mock market price
    Replace with NSE / yfinance later
    """
    return {
        "symbol": symbol,
        "ltp": round(random.uniform(100, 3000), 2),
    }
