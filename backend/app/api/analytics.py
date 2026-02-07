from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.session import SessionLocal
from app.db.models import Trade, Position


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def analytics(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    trades = (
        db.query(Trade)
        .filter(
            Trade.user_id == user.id,
            Trade.status == "CLOSED"
        )
        .all()
    )

    total = len(trades)

    if total == 0:
        return {
            "total_trades": 0,
            "wins": 0,
            "losses": 0,
            "win_rate": 0,
            "total_pnl": 0,
            "avg_win": 0,
            "avg_loss": 0,
            "expectancy": 0,
            "unrealized_pnl": 0
        }


    wins = []
    losses = []


    for t in trades:

        if t.realized_pnl > 0:
            wins.append(t.realized_pnl)
        else:
            losses.append(abs(t.realized_pnl))


    total_profit = sum(wins)
    total_loss = sum(losses)

    win_rate = len(wins) / total * 100

    avg_win = total_profit / len(wins) if wins else 0
    avg_loss = total_loss / len(losses) if losses else 0

    expectancy = (total_profit - total_loss) / total


    # Unrealized PnL
    positions = (
        db.query(Position)
        .filter(Position.user_id == user.id)
        .all()
    )

    unrealized = sum(
        float(p.unrealized_pnl or 0)
        for p in positions
    )


    return {
        "total_trades": total,
        "wins": len(wins),
        "losses": len(losses),
        "win_rate": round(win_rate, 2),
        "total_pnl": round(total_profit - total_loss, 2),
        "avg_win": round(avg_win, 2),
        "avg_loss": round(avg_loss, 2),
        "expectancy": round(expectancy, 2),
        "unrealized_pnl": round(unrealized, 2)
    }
