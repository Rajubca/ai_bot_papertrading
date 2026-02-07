import requests
from fastapi import APIRouter, HTTPException

router = APIRouter()


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json,text/plain,*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/",
    "Origin": "https://www.nseindia.com",
    "Connection": "keep-alive"
}


SESSION = requests.Session()
SESSION.headers.update(HEADERS)


def fetch_nse(symbol: str):

    # Step 1: Get cookies (mandatory)
    SESSION.get("https://www.nseindia.com", timeout=10)

    # Step 2: Fetch quote
    url = "https://www.nseindia.com/api/quote-equity"

    params = {
        "symbol": symbol
    }

    res = SESSION.get(url, params=params, timeout=10)

    if res.status_code != 200:
        return None

    return res.json()


@router.get("/quote")
def get_quote(symbol: str):

    symbol = symbol.upper()

    try:
        data = fetch_nse(symbol)

        if not data:
            raise HTTPException(502, "NSE API failed")

        price = (
            data.get("priceInfo", {})
                .get("lastPrice")
        )

        if price is None:
            raise HTTPException(404, "Price unavailable")

        return {
            "symbol": symbol,
            "ltp": round(float(price), 2),
            "source": "nseindia",
            "is_stale": True
        }

    except HTTPException:
        raise

    except Exception as e:
        print("NSE Error:", e)

        raise HTTPException(503, "Market data unavailable")
