import sys
import os

# Add the project root to the python path so imports work
sys.path.append(os.getcwd())

from database.connection import engine
from src.data.models import Base

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    init_db()
