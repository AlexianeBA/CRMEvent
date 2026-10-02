from typing import Literal

from pydantic import BaseModel


SearchResultType = Literal["company", "contact", "opportunity", "event", "quote", "invoice"]


class GlobalSearchItem(BaseModel):
    id: int
    type: SearchResultType
    title: str
    subtitle: str | None = None
    url: str


class GlobalSearchResponse(BaseModel):
    results: list[GlobalSearchItem]

