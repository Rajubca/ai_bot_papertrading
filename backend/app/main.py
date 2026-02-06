from fastapi import FastAPI

from app.api import auth, trade, portfolio, pnl, analytics, chat, reports
from app.api import _groq_test
from app.api.market import router as market_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Trading Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific Streamlit URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app = FastAPI(title="AI Paper Trading Platform")

# -------- API ROUTES --------
app.include_router(auth.router, prefix="/api/auth")
app.include_router(trade.router, prefix="/api/trade")
app.include_router(portfolio.router, prefix="/api/portfolio")
app.include_router(pnl.router, prefix="/api/pnl")
app.include_router(analytics.router, prefix="/api/analytics")
app.include_router(market_router, prefix="/api/market")
app.include_router(chat.router, prefix="/api/agent")
app.include_router(reports.router, prefix="/api/reports")
app.include_router(_groq_test.router, prefix="/debug")




# -------- HEALTH CHECK --------
@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "ai-paper-trading",
    }
