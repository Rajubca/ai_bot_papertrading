from sqlalchemy.orm import Session
from app.db.models import Trade


def get_trade_stats(db: Session, user_id: int):
    trades = (
        db.query(Trade)
        .filter(Trade.user_id == user_id, Trade.status == "CLOSED")
        .all()
    )

    if not trades:
        return {
            "total_trades": 0,
            "win_rate": 0,
            "avg_win": 0,
            "avg_loss": 0,
            "expectancy": 0,
            "max_win_streak": 0,
            "max_loss_streak": 0,
        }

    pnl_list = []
    wins = []
    losses = []

    for t in trades:
        pnl = float(t.price) * t.quantity
        pnl_list.append(pnl)

        if pnl > 0:
            wins.append(pnl)
        else:
            losses.append(abs(pnl))

    total_trades = len(trades)
    win_rate = (len(wins) / total_trades) * 100 if total_trades else 0

    avg_win = sum(wins) / len(wins) if wins else 0
    avg_loss = sum(losses) / len(losses) if losses else 0

    expectancy = (win_rate / 100 * avg_win) - (
        (1 - win_rate / 100) * avg_loss
    )

    # ---- streaks ----
    max_win_streak = 0
    max_loss_streak = 0
    current_win = 0
    current_loss = 0

    for pnl in pnl_list:
        if pnl > 0:
            current_win += 1
            current_loss = 0
        else:
            current_loss += 1
            current_win = 0

        max_win_streak = max(max_win_streak, current_win)
        max_loss_streak = max(max_loss_streak, current_loss)

    return {
        "total_trades": total_trades,
        "win_rate": round(win_rate, 2),
        "avg_win": round(avg_win, 2),
        "avg_loss": round(avg_loss, 2),
        "expectancy": round(expectancy, 2),
        "max_win_streak": max_win_streak,
        "max_loss_streak": max_loss_streak,
    }
