from sqlalchemy import func
from app.db.models import Trade
from app.analytics.streaks import trade_streaks


from app.db.models import Trade, Position
from app.analytics.streaks import trade_streaks


def get_trade_stats(db, user_id, from_date=None, to_date=None):
    q = db.query(Trade).filter(
        Trade.user_id == user_id,
        Trade.side == "SELL"   # realized trades only
    )

    if from_date:
        q = q.filter(Trade.executed_at >= from_date)
    if to_date:
        q = q.filter(Trade.executed_at <= to_date)

    sell_trades = q.order_by(Trade.executed_at.asc()).all()

    wins = []
    losses = []
    pnl_list = []

    for t in sell_trades:
        # Fetch average price from historical position snapshot
        position = (
            db.query(Position)
            .filter(Position.user_id == user_id, Position.symbol == t.symbol)
            .first()
        )

        if not position:
            continue  # safety

        avg_buy_price = position.avg_price
        pnl = (t.price - avg_buy_price) * t.quantity

        pnl_list.append(pnl)

        if pnl > 0:
            wins.append(pnl)
        else:
            losses.append(abs(pnl))

    total_trades = len(wins) + len(losses)

    win_rate = (len(wins) / total_trades * 100) if total_trades else 0
    avg_win = sum(wins) / len(wins) if wins else 0
    avg_loss = sum(losses) / len(losses) if losses else 0

    expectancy = (
        (win_rate / 100) * avg_win
        - ((1 - win_rate / 100) * avg_loss)
    )

    streaks = trade_streaks(pnl_list)

    return {
        "total_trades": total_trades,
        "win_rate": round(win_rate, 2),
        "avg_win": round(avg_win, 2),
        "avg_loss": round(avg_loss, 2),
        "expectancy": round(expectancy, 2),
        "max_win_streak": streaks["max_win_streak"],
        "max_loss_streak": streaks["max_loss_streak"]
    }
