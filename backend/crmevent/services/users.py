from passlib.context import CryptContext
from sqlalchemy.orm import Session
from crmevent.models.users import Users
from fastapi import HTTPException

from crmevent.schemas.users import UsersCreate, UserAdminCreate, UserAdminUpdate

pwd_context = CryptContext(
    schemes=["bcrypt_sha256", "bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, data: UsersCreate, role: str = "commercial", is_active: bool = True):
    user = Users(
        email=data.email,
        password_hash=hash_password(data.password),
        is_active=int(is_active),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_user_by_admin(db: Session, data: UserAdminCreate):
    if db.query(Users).filter(Users.email == data.email).first():
        raise HTTPException(status_code=409, detail="Cette adresse email est déjà utilisée")
    return create_user(db, data, data.role.value, data.is_active)


def update_user_by_admin(db: Session, user_id: int, data: UserAdminUpdate, current_user: Users):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    payload = data.model_dump(exclude_unset=True)
    if user.id == current_user.id and payload.get("is_active") is False:
        raise HTTPException(status_code=400, detail="Vous ne pouvez pas désactiver votre propre compte")
    if user.id == current_user.id and payload.get("role") not in {None, "admin"}:
        raise HTTPException(status_code=400, detail="Vous ne pouvez pas retirer votre propre rôle administrateur")

    if "role" in payload:
        user.role = payload["role"].value
    if "is_active" in payload:
        user.is_active = int(payload["is_active"])

    db.commit()
    db.refresh(user)
    return user


def reset_user_password(db: Session, user_id: int, password: str):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    user.password_hash = hash_password(password)
    db.commit()
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
