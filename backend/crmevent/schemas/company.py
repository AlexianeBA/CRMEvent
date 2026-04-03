from pydantic import BaseModel

class CompanyBase(BaseModel):
    name: str
    city: str | None = None

class CompanyCreate(CompanyBase):
    pass

class CompanyRead(CompanyBase):
    id: int

    class Config:
        from_attributes = True