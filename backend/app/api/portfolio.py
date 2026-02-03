from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.auth.dependencies import get_current_user
from app.db.models import Position, User

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("")
def get_portfolio(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    user_row = db.query(User).filter(User.id == user["id"]).first()
    positions = db.query(Position).filter(Position.user_id == user["id"]).all()

    return {
        "balance": float(user_row.balance) if user_row else 0,
        "positions": [
            {
                "symbol": p.symbol,
                "net_quantity": p.net_quantity,
                "avg_price": float(p.avg_price),
                "unrealized_pnl": float(p.unrealized_pnl),
            }
            for p in positions
        ],
    }
