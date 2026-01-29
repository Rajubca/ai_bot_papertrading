from fastapi import APIRouter, Query
from app.market.price import get_live_price

router = APIRouter()

@router.get("/quote")
def get_quote(symbol: str = Query(...)):
    price = get_live_price(symbol.upper())
    return {
        "symbol": symbol.upper(),
        "ltp": price
    }
