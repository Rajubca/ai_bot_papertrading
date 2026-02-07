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
    
    market = get_quote(symbol)
    if not market or not market.get("ltp"):
        raise HTTPException(400, "Price fetch failed")
    
    price = Decimal(str(market.get("ltp")))
    total_value = (price * Decimal(quantity)).quantize(Decimal("0.01"))

    try:
        # 1. Singular Query for an existing OPEN position
        trade = db.query(Trade).filter(
            Trade.user_id == user.id, 
            Trade.symbol == symbol, 
            Trade.status == "OPEN"
        ).first()

        if side == "BUY":
            # Check balance for fresh buys or adding to long
            # (Note: In a more complex model, buying to cover a short might not need balance)
            if user.balance < total_value:
                raise HTTPException(400, "Insufficient balance")
            
            user.balance -= total_value

            if trade:
                if trade.side == "BUY":
                    # Scenario: Add to existing Long
                    new_qty = trade.quantity + quantity
                    total_cost = (trade.entry_price * trade.quantity) + (price * quantity)
                    trade.entry_price = (total_cost / new_qty).quantize(Decimal("0.01"))
                    trade.quantity = new_qty
                else:
                    # Scenario: Buy to Cover (Reducing a Short)
                    if trade.quantity < quantity:
                        raise HTTPException(400, f"Cannot buy more than shorted quantity ({trade.quantity})")
                    trade.quantity -= quantity
                    if trade.quantity == 0:
                        trade.status = "CLOSED"
                        trade.closed_at = datetime.utcnow()
            else:
                # Scenario: Fresh Long Position
                db.add(Trade(
                    user_id=user.id, symbol=symbol, side="BUY",
                    quantity=quantity, entry_price=price, status="OPEN",
                    opened_at=datetime.utcnow()
                ))

        elif side == "SELL":
            if trade:
                if trade.side == "BUY":
                    # Scenario: Sell to Close (Reducing a Long)
                    if trade.quantity < quantity:
                        raise HTTPException(400, f"Insufficient shares. You have {trade.quantity}.")
                    
                    trade.quantity -= quantity
                    user.balance = (user.balance + total_value).quantize(Decimal("0.01"))
                    
                    if trade.quantity == 0:
                        trade.status = "CLOSED"
                        trade.closed_at = datetime.utcnow()
                        trade.exit_price = price
                else:
                    # Scenario: Sell to Open (Adding to existing Short)
                    new_qty = trade.quantity + quantity
                    total_cost = (trade.entry_price * trade.quantity) + (price * quantity)
                    trade.entry_price = (total_cost / new_qty).quantize(Decimal("0.01"))
                    trade.quantity = new_qty
                    user.balance = (user.balance + total_value).quantize(Decimal("0.01"))
            else:
                # Scenario: Fresh Short Position
                db.add(Trade(
                    user_id=user.id, symbol=symbol, side="SELL",
                    quantity=quantity, entry_price=price, status="OPEN",
                    opened_at=datetime.utcnow()
                ))
                user.balance = (user.balance + total_value).quantize(Decimal("0.01"))

        db.commit()
        return {"status": "success", "balance": float(user.balance)}

    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Transaction failed: {str(e)}")

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
    # ================= SELL =================
    else:
        if pos:
            # If they have a long position, this reduces it (Sell to Close)
            # If they have no position or are already short, this adds to short (Sell to Open)
            pos.net_quantity -= quantity
        else:
            # Fresh Short Position
            db.add(Position(
                user_id=user_id,
                symbol=symbol,
                net_quantity=-quantity,
                avg_price=price
            ))


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

