from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from crmevent.db.base import get_db
from crmevent.schemas.users import UsersCreate, UsersRead
from crmevent.services import users as service
from crmevent.core.security import create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UsersRead, status_code=status.HTTP_201_CREATED)
def register(data: UsersCreate, db: Session = Depends(get_db)):
    return service.create_user(db, data)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    email = form_data.username
    user = service.authenticate_user(db, email, form_data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.get("users/list", response_model=list[UsersRead])
def list_users(db: Session = Depends(get_db)):
    return db.query(service.Users).all()


@router.get("/me")
def me(current_user = Depends(get_current_user)):
    return current_user