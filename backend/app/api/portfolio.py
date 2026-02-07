from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.session import SessionLocal
from app.db.models import Position, User

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_portfolio(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    positions = (
        db.query(Position)
        .filter(Position.user_id == user.id)
        .all()
    )

    data = []

    for p in positions:
        data.append({
            "symbol": p.symbol,
            "quantity": p.net_quantity,
            "avg_price": round(float(p.avg_price), 2)
        })

    return {
        "balance": round(float(user.balance), 2),
        "positions": data
    }
