from enum import Enum

from pydantic import BaseModel, Field


class UserRole(str, Enum):
    admin = "admin"
    manager = "manager"
    commercial = "commercial"
    comptable = "comptable"

class UsersBase(BaseModel):
    email: str
    

class UsersCreate(UsersBase):
    password: str = Field(min_length=8, max_length=256)

class UsersRead(UsersBase):
    id: int
    is_active: int
    role: UserRole

    class Config:
        from_attributes = True


class UserAdminCreate(UsersCreate):
    role: UserRole = UserRole.commercial
    is_active: bool = True


class UserAdminUpdate(BaseModel):
    role: UserRole | None = None
    is_active: bool | None = None


class UserPasswordReset(BaseModel):
    password: str = Field(min_length=8, max_length=256)
