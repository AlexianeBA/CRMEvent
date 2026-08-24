from pydantic import BaseModel, Field

class ContactBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=3, max_length=255)
    phone_number: str | None = Field(default=None, max_length=20)
    company_id: int | None = Field(default=None, gt=0)

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    email: str | None = Field(default=None, max_length=100)
    phone_number: str | None = Field(default=None, max_length=20)
    company_id: int | None = Field(default=None, gt=0)

class ContactCompanyRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class ContactRead(ContactBase):
    id: int
    company: ContactCompanyRead | None = None

    class Config:
        from_attributes = True
