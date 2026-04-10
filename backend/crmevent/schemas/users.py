from pydantic import BaseModel, Field

class UsersBase(BaseModel):
    email: str
    

class UsersCreate(UsersBase):
    password: str = Field(min_length=8, max_length=256)

class UsersRead(UsersBase):
    id: int
    is_active: int

    class Config:
        from_attributes = True