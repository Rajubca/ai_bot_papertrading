from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.auth.dependencies import get_current_user
from app.db.models import Trade

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/trades")
def trade_report(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    trades = db.query(Trade).filter(Trade.user_id == user["id"]).all()

    return [
        {
            "id": t.id,
            "symbol": t.symbol,
            "side": t.side,
            "qty": t.quantity,
            "price": float(t.price),
            "status": t.status,
            "executed_at": str(t.executed_at),
        }
        for t in trades
    ]
