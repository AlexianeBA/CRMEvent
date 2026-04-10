from passlib.context import CryptContext
from sqlalchemy.orm import Session
from crmevent.models.users import Users
from crmevent.schemas.users import UsersCreate

pwd_context = CryptContext(
    schemes=["bcrypt_sha256", "bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, data: UsersCreate):
    user = Users(
        email=data.email,
        password_hash=hash_password(data.password),
        is_active=1,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

