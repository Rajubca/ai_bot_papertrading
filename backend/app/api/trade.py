from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.session import SessionLocal
from app.auth.dependencies import get_current_user
from app.trading.engine import execute_trade

router = APIRouter()


class TradeRequest(BaseModel):
    symbol: str
    side: str  # BUY / SELL
    quantity: int
    trade_notes: str | None = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("")
def place_trade(
    payload: TradeRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if payload.side not in ("BUY", "SELL"):
        raise HTTPException(status_code=400, detail="Invalid side")

    return execute_trade(
        db=db,
        user_id=user["id"],
        symbol=payload.symbol,
        side=payload.side,
        quantity=payload.quantity,
        price=100.0,  # mock price
        payload={"trade_notes": payload.trade_notes},
    )
