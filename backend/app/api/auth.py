from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


# --------------------
# Schemas
# --------------------
class LoginRequest(BaseModel):
    email: str
    password: str


# --------------------
# Routes
# --------------------
@router.post("/login")
def login(payload: LoginRequest):
    """
    TEMP DEV LOGIN
    Replace with real password check later
    """
    if payload.email == "demo@test.com" and payload.password == "demo":
        return {
            "access_token": "dev-token",
            "token_type": "bearer"
        }

    raise HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/register")
def register():
    """
    TEMP DEV REGISTER
    """
    return {"status": "ok"}
