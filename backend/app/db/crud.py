from app.db.models import User, Trade, Position
from app.db.models import Position

def get_position(db, user_id, symbol):
    return (
        db.query(Position)
        .filter(Position.user_id == user_id, Position.symbol == symbol)
        .first()
    )

def get_user(db, user_id):
    return db.query(User).filter(User.id == user_id).first()

def update_user_balance(db, user):
    db.add(user)
    db.commit()

def create_trade(db, user_id, symbol, side, quantity, price, payload):
    trade = Trade(
        user_id=user_id,
        symbol=symbol,
        side=side,
        quantity=quantity,
        price=price,
        order_type=payload.get("order_type", "MARKET"),
        sl=payload.get("sl"),
        target=payload.get("target"),
        trade_notes=payload.get("trade_notes")
    )
    db.add(trade)
    db.commit()
    db.refresh(trade)
    return trade

def update_position(db, user_id, symbol, side, quantity, price):
    position = db.query(Position).filter_by(
        user_id=user_id,
        symbol=symbol
    ).first()

    if not position:
        net_qty = quantity if side == "BUY" else -quantity
        avg_price = price
        position = Position(
            user_id=user_id,
            symbol=symbol,
            net_quantity=net_qty,
            avg_price=avg_price
        )
        db.add(position)

    else:
        total_qty = position.net_quantity + (quantity if side == "BUY" else -quantity)

        if total_qty == 0:
            db.delete(position)
            db.commit()
            return

        position.avg_price = (
            (position.avg_price * position.net_quantity) + (price * quantity)
        ) / total_qty

        position.net_quantity = total_qty
        db.add(position)

    db.commit()
