import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from crmevent.routers import (
    company as company_router,
    users as users_router,
    contact as contact_router,
    opportunity as opportunity_router,
    activity as activity_router,
    event as event_router,
    quote as quote_router,
    invoice as invoice_router,
    history as history_router,
    notification as notification_router,
    task as task_router,
    search as search_router,
)
from crmevent.db.base import Base
from crmevent.db.session import engine

from crmevent.models.company import Company
from crmevent.models.users import Users
from crmevent.models.contact import Contact
from crmevent.models.opportunity import Opportunity
from crmevent.models.activity import Activity
from crmevent.models.event import Event
from crmevent.models.quote import Quote, QuoteLine
from crmevent.models.invoice import Invoice, InvoicePayment, InvoiceLine
from crmevent.models.document_sequence import DocumentSequence
from crmevent.models.history import HistoryEntry
from crmevent.models.notification import Notification
from crmevent.models.task import Task
from crmevent.services.notification_scheduler import notification_scheduler

app = FastAPI(
    title="CRM API",
    description="API CRM Event",
    version="1.0.0",
    docs_url="/docs",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)
app.include_router(company_router.router)
app.include_router(users_router.router)
app.include_router(contact_router.router)
app.include_router(opportunity_router.router)
app.include_router(activity_router.router)
app.include_router(event_router.router)
app.include_router(quote_router.router)
app.include_router(invoice_router.router)
app.include_router(history_router.router)
app.include_router(notification_router.router)
app.include_router(task_router.router)
app.include_router(search_router.router)
@app.get("/")
def root():
    return {"message": "Bienvenue dans le CRM API"}

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    app.state.notification_scheduler = asyncio.create_task(notification_scheduler())


@app.on_event("shutdown")
async def on_shutdown():
    scheduler = getattr(app.state, "notification_scheduler", None)
    if scheduler:
        scheduler.cancel()
        try:
            await scheduler
        except asyncio.CancelledError:
            pass
