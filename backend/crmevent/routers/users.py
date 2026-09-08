from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from crmevent.db.base import get_db
from crmevent.schemas.users import OwnPasswordChange, UsersCreate, UsersRead, UserAdminCreate, UserAdminUpdate, UserPasswordReset
from crmevent.services import users as service
from crmevent.core.security import create_access_token, get_current_user, require_roles
from crmevent.models.users import Users

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UsersRead, status_code=status.HTTP_201_CREATED)
def register(data: UsersCreate, db: Session = Depends(get_db)):
    if db.query(Users).count() > 0:
        raise HTTPException(status_code=403, detail="L'inscription publique est fermée. Contactez un administrateur")
    existing_user = db.query(Users).filter(Users.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return service.create_user(db, data, role="admin")


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

@router.get("/users/list", response_model=list[UsersRead])
def list_users(db: Session = Depends(get_db), current_user=Depends(require_roles("admin"))):
    return db.query(service.Users).all()


@router.get("/me", response_model=UsersRead)
def me(current_user = Depends(get_current_user)):
    return current_user


@router.post("/me/change-password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(data: OwnPasswordChange, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    service.change_own_password(db, current_user, data.current_password, data.new_password)


@router.post("/users", response_model=UsersRead, status_code=status.HTTP_201_CREATED)
def create_user(data: UserAdminCreate, db: Session = Depends(get_db), current_user=Depends(require_roles("admin"))):
    return service.create_user_by_admin(db, data)


@router.patch("/users/{user_id}", response_model=UsersRead)
def update_user(user_id: int, data: UserAdminUpdate, db: Session = Depends(get_db), current_user=Depends(require_roles("admin"))):
    return service.update_user_by_admin(db, user_id, data, current_user)


@router.post("/users/{user_id}/reset-password", status_code=status.HTTP_204_NO_CONTENT)
def reset_password(user_id: int, data: UserPasswordReset, db: Session = Depends(get_db), current_user=Depends(require_roles("admin"))):
    service.reset_user_password(db, user_id, data.password)
