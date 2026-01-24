import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

# Default to SQLite if no URL is provided
# Using a local Windows path to avoid locking issues with SQLite on WSL shares
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///C:/Users/Aliihsan/stock_portfolio_mcp.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
