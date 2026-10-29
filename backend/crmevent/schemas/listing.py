from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


class ListParams(BaseModel):
    q: str = Field(default="", max_length=100)
    status: str | None = Field(default=None, max_length=50)
    company_id: int | None = Field(default=None, gt=0)
    commercial_id: int | None = Field(default=None, gt=0)
    date_from: date | None = None
    date_to: date | None = None
    opportunity_id: int | None = Field(default=None, gt=0)
    contact_id: int | None = Field(default=None, gt=0)
    event_id: int | None = Field(default=None, gt=0)
    quote_id: int | None = Field(default=None, gt=0)
    invoice_id: int | None = Field(default=None, gt=0)
    sort_by: str = Field(default="id", max_length=50)
    sort_order: Literal["asc", "desc"] = "desc"
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class ExportParams(ListParams):
    format: Literal["csv", "xlsx"] = "csv"
