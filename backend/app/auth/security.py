from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str) -> str:
    # bcrypt max = 72 bytes
    safe_password = password.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.hash(safe_password)

def verify_password(plain: str, hashed: str) -> bool:
    safe_plain = plain.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return pwd_context.verify(safe_plain, hashed)
