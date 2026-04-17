from fastapi import FastAPI
from crmevent.routers import company, users, contact

app = FastAPI(
    title="CRM API",
    description="API CRM Event",
    version="1.0.0",
    docs_url="/docs",
)

app.include_router(company.router)
app.include_router(users.router)
app.include_router(contact.router)

@app.get("/")
def root():
    return {"message": "Bienvenue dans le CRM API"}