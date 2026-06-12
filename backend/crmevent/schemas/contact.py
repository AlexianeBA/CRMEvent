from pydantic import BaseModel

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str | None = None
    phone_number: str | None = None
    company_id: int | None = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    company_id: int | None = None

class ContactRead(ContactBase):
    id: int

    class Config:
        from_attributes = True

