from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.db.session import SessionLocal
from app.auth.dependencies import get_current_user
from app.db.models import DailyPNL, Trade






router = APIRouter()




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/today")
def get_today_pnl(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    """
    Returns today's PnL (realized + unrealized)
    """

    today = date.today()

    row = (
        db.query(DailyPNL)
        .filter(
            DailyPNL.user_id == user["id"],
            DailyPNL.trade_date == today,
        )
        .first()
    )

    if row:
        return {
            "date": str(today),
            "realized_pnl": float(row.realized_pnl),
            "unrealized_pnl": float(row.unrealized_pnl),
            "total_pnl": float(row.realized_pnl + row.unrealized_pnl),
        }

    # fallback: calculate realized pnl from closed trades today
    trades = (
        db.query(Trade)
        .filter(
            Trade.user_id == user["id"],
            Trade.status == "CLOSED",
            Trade.executed_at >= today,
        )
        .all()
    )

    realized = sum(
        float(t.price * t.quantity)
        for t in trades
        if t.side == "SELL"
    )

    return {
        "date": str(today),
        "realized_pnl": realized,
        "unrealized_pnl": 0.0,
        "total_pnl": realized,
    }
