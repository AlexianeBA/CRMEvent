from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./crm.db")
print(f"Using database URL: {DATABASE_URL}")
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)