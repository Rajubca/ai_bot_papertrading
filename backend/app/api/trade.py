from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from app.db.session import get_db
from app.db.models import User, Trade, Position
from app.api.market import get_quote
from app.auth.dependencies import get_current_user


router = APIRouter()


# ===============================
# Request Schema
# ===============================

class TradeRequest(BaseModel):
    symbol: str
    quantity: int
    side: str
    trade_notes: Optional[str] = None


# ===============================
# Execute Trade
# ===============================

@router.post("/execute")
def execute_trade(
    order: TradeRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    symbol = order.symbol.upper()
    quantity = order.quantity
    side = order.side.upper()

    if quantity <= 0:
        raise HTTPException(400, "Quantity must be > 0")

    if side not in ["BUY", "SELL"]:
        raise HTTPException(400, "Invalid side")

    # Fetch price
    market = get_quote(symbol)

    if not market or not market.get("ltp"):
        raise HTTPException(400, "Price fetch failed")

    price = Decimal(str(market.get("ltp")))
    qty = Decimal(quantity)

    total_value = (price * qty).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )



    try:

        # ================= BUY =================
        if side == "BUY":

            if user.balance < total_value:
                raise HTTPException(400, "Insufficient balance")

            user.balance = (user.balance - total_value).quantize(
                Decimal("0.01")
            )


            update_position(
                db, user.id, symbol, quantity, price, True
            )


        # ================= SELL =================
        else:

            user.balance = (user.balance + total_value).quantize(
                Decimal("0.01")
            )


            update_position(
                db, user.id, symbol, quantity, price, False
            )


        # Save trade
        trade = Trade(
            user_id=user.id,
            symbol=symbol,
            side=side,
            quantity=quantity,
            entry_price=price,
            status="OPEN",
            trade_notes=order.trade_notes,
            opened_at=datetime.utcnow()
        )

        db.add(trade)
        db.commit()
        db.refresh(trade)

        return {
            "status": "success",
            "symbol": symbol,
            "side": side,
            "qty": quantity,
            "trade_id": trade.id,
            "price": price,
            "balance": round(float(user.balance), 2)
        }


    except HTTPException:
        db.rollback()
        raise

    except Exception as e:

        db.rollback()
        print("Trade Error:", e)

        raise HTTPException(500, "Trade failed")


# ===============================
# Close Trade (Square Off)
# ===============================

@router.post("/close")
def close_trade(
    symbol: str,
    quantity: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    symbol = symbol.upper()

    market = get_quote(symbol)

    if not market or not market.get("ltp"):
        raise HTTPException(400, "Price fetch failed")

    exit_price = Decimal(str(market["ltp"]))


    trades = (
        db.query(Trade)
        .filter(
            Trade.user_id == user.id,
            Trade.symbol == symbol,
            Trade.status == "OPEN"
        )
        .order_by(Trade.opened_at)
        .all()
    )

    if not trades:
        raise HTTPException(400, "No open trades")
    open_qty = sum(t.quantity for t in trades)

    if quantity > open_qty:
        raise HTTPException(400, "Close quantity exceeds open position")

    remaining = quantity
    total_pnl = Decimal("0.00")



    for t in trades:

        if remaining <= 0:
            break

        close_qty = min(t.quantity, remaining)

        t.quantity -= close_qty

        # Long
        entry = Decimal(str(t.entry_price))
        qty = Decimal(close_qty)

        # Long
        if t.side == "BUY":
            pnl = (exit_price - entry) * qty

        # Short
        else:
            pnl = (entry - exit_price) * qty


        pnl = pnl.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        t.realized_pnl = (Decimal(str(t.realized_pnl or 0)) + pnl).quantize(
            Decimal("0.01")
        )

        total_pnl += pnl

        if t.quantity == 0:

            t.exit_price = exit_price
            t.closed_at = datetime.utcnow()
            t.status = "CLOSED"


        # Update Position
        pos = (
            db.query(Position)
            .filter_by(user_id=user.id, symbol=symbol)
            .first()
        )

        if pos:

            if pos.net_quantity > 0:
                pos.net_quantity -= close_qty
            else:
                pos.net_quantity += close_qty

            if pos.net_quantity == 0:
                db.delete(pos)


        remaining -= close_qty


    user.balance = (user.balance + total_pnl).quantize(
                        Decimal("0.01")
                    )


    db.commit()

    return {
        "status": "closed",
        "pnl": round(total_pnl, 2),
        "balance": round(float(user.balance), 2)
    }


# ===============================
# Position Manager
# ===============================

def update_position(
    db,
    user_id,
    symbol,
    quantity,
    price,
    is_buy: bool
):

    pos = (
        db.query(Position)
        .filter_by(user_id=user_id, symbol=symbol)
        .first()
    )


    # ================= BUY =================
    if is_buy:

        if pos:

            # Cover short
            if pos.net_quantity < 0:

                pos.net_quantity += quantity

                if pos.net_quantity == 0:
                    pos.avg_price = Decimal("0.00")



            # Add long
            else:

                total_qty = Decimal(pos.net_quantity + quantity)

                total_cost = (
                    Decimal(str(pos.avg_price)) * Decimal(pos.net_quantity)
                    + price * Decimal(quantity)
                )

                pos.avg_price = (total_cost / total_qty).quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )

                pos.net_quantity = int(total_qty)



        else:

            db.add(Position(
                user_id=user_id,
                symbol=symbol,
                net_quantity=quantity,
                avg_price=price
            ))


    # ================= SELL =================
    else:

        pos = (
            db.query(Position)
            .filter_by(user_id=user.id, symbol=symbol)
            .first()
        )

        # Prevent naked short beyond limit (optional)
        if pos and pos.net_quantity < 0:
            max_short = abs(pos.net_quantity) + quantity

            if max_short > 1000:   # example limit
                raise HTTPException(400, "Short limit exceeded")



    # Update MTM
    pos = (
        db.query(Position)
        .filter_by(user_id=user_id, symbol=symbol)
        .first()
    )

    if pos:

        if pos.net_quantity > 0:

            pos.unrealized_pnl = (
                (price - pos.avg_price) * Decimal(pos.net_quantity)
            ).quantize(Decimal("0.01"))


        else:

            pos.unrealized_pnl = (
                (pos.avg_price - price) * Decimal(abs(pos.net_quantity))
            ).quantize(Decimal("0.01"))

