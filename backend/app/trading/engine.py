from app.db import crud
from app.market.price import get_live_price


def execute_trade(db, user_id, symbol, side, quantity, payload):
    """
    Core paper-trade execution engine.
    - Fetches live market price internally
    - Updates trades, balance, positions
    """

    # 1️⃣ Fetch user
    user = crud.get_user(db, user_id)
    if not user:
        raise ValueError("Invalid user")

    symbol = symbol.upper()
    side = side.upper()

    # 2️⃣ Fetch live market price (REAL DATA)
    price = get_live_price(symbol)

    trade_value = price * quantity

    # 3️⃣ BUY validation
    if side == "BUY" and user.balance < trade_value:
        raise ValueError("Insufficient balance")

    # 4️⃣ SELL validation (position check)
    if side == "SELL":
        position = crud.get_position(db, user_id, symbol)
        if not position or position.net_quantity < quantity:
            raise ValueError("Insufficient quantity to sell")

    # 5️⃣ Insert trade
    trade = crud.create_trade(
        db=db,
        user_id=user_id,
        symbol=symbol,
        side=side,
        quantity=quantity,
        price=price,
        payload=payload
    )

    # 6️⃣ Update balance
    if side == "BUY":
        user.balance -= trade_value
    else:
        user.balance += trade_value

    crud.update_user_balance(db, user)

    # 7️⃣ Update position
    crud.update_position(
        db=db,
        user_id=user_id,
        symbol=symbol,
        side=side,
        quantity=quantity,
        price=price
    )

    return {
        "status": "SUCCESS",
        "trade_id": trade.id,
        "symbol": symbol,
        "side": side,
        "executed_price": price,
        "quantity": quantity,
        "remaining_balance": float(user.balance)
    }
