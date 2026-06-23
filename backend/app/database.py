from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Creates a file called 'livestock.db' right next to your backend folder
SQLALCHEMY_DATABASE_URL = "sqlite:///./livestock.db"

# Connect_args needed for SQLite to handle multiple threads
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency: This gets used in main.py to give each API request its own database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()