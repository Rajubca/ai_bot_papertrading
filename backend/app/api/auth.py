from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.auth.jwt import create_access_token

from app.db.session import SessionLocal
from app.db.models import User
from app.auth.security import hash_password, verify_password

router = APIRouter()


# ---------- Schemas ----------
class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ---------- DB ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------- REGISTER ----------

@router.post("/register")
def register_user(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
):
    try:
        existing = db.query(User).filter(User.email == payload.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        user = User(
            name=payload.name,
            email=payload.email,
            password_hash=hash_password(payload.password),
            balance=100000.00,
            status="ACTIVE",
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return {
            "message": "User created successfully",
            "user_id": user.id,
            "email": user.email,
        }

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Registration failed: {str(e)}"
        )


# ---------- LOGIN ----------
@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer",
        "user_id": user.id,
    }

