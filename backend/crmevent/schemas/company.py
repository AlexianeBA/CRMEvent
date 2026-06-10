from pydantic import BaseModel

class CompanyBase(BaseModel):
    name: str
    city: str | None = None

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: str | None = None
    city: str | None = None
    address: str | None = None

class CompanyRead(CompanyBase):
    id: int
    address: str | None = None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True