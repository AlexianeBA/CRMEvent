from pydantic import BaseModel


class HistoryRead(BaseModel):
    id: int
    action: str
    entity_type: str
    entity_id: int
    entity_label: str
    message: str
    user_id: int
    user_email: str
    company_id: int | None = None
    contact_id: int | None = None
    opportunity_id: int | None = None
    event_id: int | None = None
    quote_id: int | None = None
    invoice_id: int | None = None
    created_at: str

    class Config:
        from_attributes = True
