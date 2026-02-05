from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.auth.dependencies import decode_access_token as decode_token
from app.db.session import SessionLocal
from app.db.models import DailyPNL

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/today")
def get_today_pnl(
    user=Depends(decode_token),
    db: Session = Depends(get_db),
):
    today = date.today()

    pnl = (
        db.query(DailyPNL)
        .filter(
            DailyPNL.user_id == user["id"],
            DailyPNL.trade_date == today,
        )
        .first()
    )

    if not pnl:
        return {
            "realized_pnl": 0,
            "unrealized_pnl": 0,
            "total_pnl": 0,
        }

    total = float(pnl.realized_pnl) + float(pnl.unrealized_pnl)

    return {
        "realized_pnl": float(pnl.realized_pnl),
        "unrealized_pnl": float(pnl.unrealized_pnl),
        "total_pnl": total,
    }
