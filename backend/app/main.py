from fastapi import FastAPI, APIRouter
from app.api import auth, trade, portfolio, pnl, chat, reports, analytics
from app.api.market import router as market_router

router = APIRouter()


app = FastAPI(title="AI Paper Trading Platform")

app.include_router(market_router, prefix="/api/market")
app.include_router(auth.router, prefix="/api/auth")
app.include_router(trade.router, prefix="/api/trade")
app.include_router(portfolio.router, prefix="/api/portfolio")
app.include_router(pnl.router, prefix="/api/pnl")
app.include_router(chat.router, prefix="/api/agent")
app.include_router(reports.router, prefix="/api/reports")
app.include_router(analytics.router, prefix="/api/analytics")
