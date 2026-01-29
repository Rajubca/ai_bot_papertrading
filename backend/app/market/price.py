import yfinance as yf
from app.config import settings


def get_live_price(symbol: str) -> float:
    """
    Returns latest available price for NSE stocks.
    Example symbol: RELIANCE, INFY, TCS
    """

    provider = settings.MARKET_DATA_PROVIDER

    if provider == "yfinance":
        return _from_yfinance(symbol)

    raise ValueError("Invalid MARKET_DATA_PROVIDER")


def _from_yfinance(symbol: str) -> float:
    ticker = yf.Ticker(f"{symbol}.NS")

    data = ticker.history(period="1d", interval="1m")

    if data.empty:
        raise ValueError(f"No market data for {symbol}")

    return round(float(data["Close"].iloc[-1]), 2)
