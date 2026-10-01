from pydantic import BaseModel, Field
from crmevent.schemas.contact import ContactRead

class CompanyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    address: str | None = Field(default=None, max_length=255)
    postal_code: str | None = Field(default=None, max_length=20)
    city: str | None = Field(default=None, max_length=255)
    country: str | None = Field(default="France", max_length=100)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    siret: str | None = Field(default=None, max_length=20)
    vat_number: str | None = Field(default=None, max_length=30)

class CompanyCreate(CompanyBase):
    contact_ids: list[int] = Field(default_factory=list)

class CompanyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    city: str | None = Field(default=None, max_length=255)
    address: str | None = Field(default=None, max_length=255)
    postal_code: str | None = Field(default=None, max_length=20)
    country: str | None = Field(default=None, max_length=100)
    email: str | None = Field(default=None, max_length=255)
    phone: str | None = Field(default=None, max_length=50)
    siret: str | None = Field(default=None, max_length=20)
    vat_number: str | None = Field(default=None, max_length=30)
    contact_ids: list[int] | None = None

class CompanyRead(CompanyBase):
    id: int
    contacts: list["ContactRead"] = Field(default_factory=list)
    created_at: str = Field(..., min_length=1, max_length=255)
    updated_at: str = Field(..., min_length=1, max_length=255)

    class Config:
        from_attributes = True
