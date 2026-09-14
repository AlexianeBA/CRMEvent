import os
import hashlib
import hmac
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from crmevent.db.base import get_db
from crmevent.models.users import Users



load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
RESET_PASSWORD_EXPIRE_MINUTES = int(os.getenv("RESET_PASSWORD_EXPIRE_MINUTES", "30"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def _password_fingerprint(password_hash: str) -> str:
    return hashlib.sha256(password_hash.encode()).hexdigest()


def create_password_reset_token(email: str, password_hash: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=RESET_PASSWORD_EXPIRE_MINUTES)
    payload = {
        "sub": email,
        "purpose": "password_reset",
        "pwd": _password_fingerprint(password_hash),
        "exp": expire,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_password_reset_token(token: str) -> tuple[str, str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        fingerprint = payload.get("pwd")
        if payload.get("purpose") != "password_reset" or not email or not fingerprint:
            raise HTTPException(status_code=400, detail="Lien de réinitialisation invalide ou expiré")
        return email, fingerprint
    except JWTError as error:
        raise HTTPException(status_code=400, detail="Lien de réinitialisation invalide ou expiré") from error


def password_fingerprint_matches(password_hash: str, fingerprint: str) -> bool:
    return hmac.compare_digest(_password_fingerprint(password_hash), fingerprint)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(Users).filter(Users.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    return user


def require_roles(*allowed_roles: str):
    def dependency(current_user: Users = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="Vous n'avez pas les droits nécessaires pour cette action",
            )
        return current_user

    return dependency
