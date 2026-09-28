import logging
import os

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func

from crmevent.db.base import get_db
from crmevent.schemas.users import ForgotPasswordRequest, ForgotPasswordReset, OwnPasswordChange, UsersCreate, UsersRead, UserAdminCreate, UserAdminUpdate, UserPasswordReset
from crmevent.services import users as service
from crmevent.core.security import RESET_PASSWORD_EXPIRE_MINUTES, create_access_token, create_password_reset_token, get_current_user, require_roles
from crmevent.models.users import Users
from crmevent.services.email import send_email

logger = logging.getLogger(__name__)

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


@router.post("/forgot-password", status_code=status.HTTP_202_ACCEPTED)
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    message = "Si cette adresse correspond à un compte actif, un email a été envoyé"
    user = db.query(Users).filter(func.lower(Users.email) == data.email.strip().lower()).first()
    if not user or not user.is_active:
        return {"detail": message}

    token = create_password_reset_token(user.email, user.password_hash)
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173").rstrip("/")
    reset_url = f"{frontend_url}/reset-password/{token}"
    try:
        send_email(
            recipient=user.email,
            subject="Réinitialisation de votre mot de passe CRMEvent",
            body=(
                "Bonjour,\n\n"
                "Une demande de réinitialisation de votre mot de passe a été effectuée.\n"
                f"Utilisez ce lien dans les {RESET_PASSWORD_EXPIRE_MINUTES} prochaines minutes :\n{reset_url}\n\n"
                "Si vous n'êtes pas à l'origine de cette demande, ignorez cet email.\n\n"
                "L'équipe CRMEvent"
            ),
        )
    except HTTPException:
        logger.exception("Échec de l'envoi de l'email de réinitialisation")
    return {"detail": message}


@router.post("/reset-password", status_code=status.HTTP_204_NO_CONTENT)
def reset_forgotten_password(data: ForgotPasswordReset, db: Session = Depends(get_db)):
    service.reset_forgotten_password(db, data.token, data.new_password)

@router.get("/users/list", response_model=list[UsersRead])
def list_users(db: Session = Depends(get_db), current_user=Depends(require_roles("admin"))):
    return db.query(service.Users).all()


@router.get("/users/options", response_model=list[UsersRead])
def list_active_user_options(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Users).filter(Users.is_active == 1).order_by(Users.email.asc()).all()


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
