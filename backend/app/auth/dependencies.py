from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    TEMP DEV USER
    Replace with real JWT decoding later
    """
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # TEMP hardcoded user
    return {
        "id": 1,
        "email": "demo@test.com",
        "role": "USER",
    }
