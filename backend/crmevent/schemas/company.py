from pydantic import BaseModel, Field
from crmevent.schemas.contact import ContactRead

class CompanyBase(BaseModel):
    name: str
    address: str | None = None
    city: str | None = None

class CompanyCreate(CompanyBase):
    contact_ids: list[int] = Field(default_factory=list)

class CompanyUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    city: str = Field(..., min_length=1, max_length=255)
    address: str = Field(..., min_length=1, max_length=255)
    contact_ids: list[int] | None = None

class CompanyRead(CompanyBase):
    id: int
    address: str = Field(..., min_length=1, max_length=255)
    contacts: list["ContactRead"] = []
    created_at: str = Field(..., min_length=1, max_length=255)
    updated_at: str = Field(..., min_length=1, max_length=255)

    class Config:
        from_attributes = True