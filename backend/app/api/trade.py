from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.auth.dependencies import get_current_user
from app.market.nse import get_price
from app.trading.engine import execute_trade
from app.db import crud

router = APIRouter()

@router.post("")
def place_trade(payload: dict, user=Depends(get_current_user)):
    db: Session = SessionLocal()
    try:
        symbol = payload["symbol"].upper()
        side = payload["side"]
        quantity = int(payload["quantity"])

        if quantity <= 0:
            raise HTTPException(400, "Invalid quantity")

        market_price = get_price(symbol)

        result = execute_trade(
            db=db,
            user_id=user["id"],
            symbol=symbol,
            side=side,
            quantity=quantity,
            price=market_price,
            payload=payload
        )

        return result

    except KeyError as e:
        raise HTTPException(400, f"Missing field {str(e)}")

    except ValueError as e:
        raise HTTPException(400, str(e))

    finally:
        db.close()
