from fastapi import APIRouter
import yfinance as yf
import time
import threading

router = APIRouter()

CACHE_TTL = 15          # seconds
STALE_TTL = 300         # 5 minutes
FAIL_COOLDOWN = 60      # seconds

_cache = {}
_last_good = {}
_failures = {}
_lock = threading.Lock()

@router.get("/quote")
def get_quote(symbol: str):
    symbol = symbol.upper()
    now = time.time()

    with _lock:
        # Serve fresh cache
        if symbol in _cache and now - _cache[symbol]["ts"] < CACHE_TTL:
            return _cache[symbol]["data"]

        # Serve stale price if Yahoo is failing
        if symbol in _failures and symbol in _last_good:
            if now - _last_good[symbol]["ts"] < STALE_TTL:
                data = dict(_last_good[symbol]["data"])
                data["stale"] = True
                return data

        # Cooldown (avoid hammering)
        if symbol in _failures and now - _failures[symbol] < FAIL_COOLDOWN:
            if symbol in _last_good:
                data = dict(_last_good[symbol]["data"])
                data["stale"] = True
                return data

    # Attempt Yahoo fetch
    try:
        ticker = yf.Ticker(f"{symbol}.NS")
        price = None

        # SAFEST method
        try:
            price = ticker.fast_info.get("last_price")
        except Exception:
            pass

        # LAST fallback (low frequency)
        if not price:
            hist = ticker.history(period="5d")
            if not hist.empty:
                price = float(hist["Close"].iloc[-1])

        if not price:
            raise RuntimeError("No price")

        data = {
            "symbol": symbol,
            "ltp": round(price, 2),
            "currency": "INR",
            "source": "Yahoo Finance",
            "delayed": True,
            "stale": False,
        }

        with _lock:
            _cache[symbol] = {"data": data, "ts": now}
            _last_good[symbol] = {"data": data, "ts": now}
            _failures.pop(symbol, None)

        return data

    except Exception:
        with _lock:
            _failures[symbol] = now

        # Return stale if available
        if symbol in _last_good:
            data = dict(_last_good[symbol]["data"])
            data["stale"] = True
            return data

        # Absolute last resort
        return {
            "symbol": symbol,
            "ltp": None,
            "currency": "INR",
            "source": "Yahoo Finance",
            "delayed": True,
            "stale": True,
            "error": "Price temporarily unavailable",
        }
