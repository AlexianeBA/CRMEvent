from sqlalchemy.orm import DeclarativeBase
from crmevent.db.session import SessionLocal

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()