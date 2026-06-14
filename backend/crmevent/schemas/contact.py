from pydantic import BaseModel, Field

class ContactBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: str | None = None
    phone_number: str | None = Field(default=None, max_length=20)
    company_id: int | None = Field(default=None, gt=0)

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    email: str | None = Field(default=None, max_length=100)
    phone_number: str | None = Field(default=None, max_length=20)
    company_id: int | None = None

class ContactRead(ContactBase):
    id: int

    class Config:
        from_attributes = True

