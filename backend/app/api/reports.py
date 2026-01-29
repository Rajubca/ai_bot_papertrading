from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user
from app.db.session import SessionLocal
from app.db.models import Trade
from app.reports.csv_report import generate_trade_csv

router = APIRouter()

@router.post("/generate")
def generate_report(payload: dict, user=Depends(get_current_user)):
    db = SessionLocal()

    trades = db.query(Trade).filter(
        Trade.user_id == user["id"],
        Trade.executed_at.between(payload["from"], payload["to"])
    ).all()

    if payload["format"] == "CSV":
        return {"data": generate_trade_csv(trades)}

    return {"status": "PDF_GENERATED"}
