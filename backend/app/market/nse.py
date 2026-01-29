# app/market/nse.py
import yfinance as yf

def get_price(symbol):
    data = yf.Ticker(symbol + ".NS")
    return data.history(period="1d")["Close"][-1]
