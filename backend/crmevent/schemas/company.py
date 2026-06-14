from pydantic import BaseModel, Field

class CompanyBase(BaseModel):
    name: str
    city: str | None = None

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    city: str = Field(..., min_length=1, max_length=255)
    address: str = Field(..., min_length=1, max_length=255)

class CompanyRead(CompanyBase):
    id: int
    address: str = Field(..., min_length=1, max_length=255)
    created_at: str = Field(..., min_length=1, max_length=255)
    updated_at: str = Field(..., min_length=1, max_length=255)

    class Config:
        from_attributes = True