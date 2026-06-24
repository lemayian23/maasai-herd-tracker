# Line 1
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
# Line 2
from sqlalchemy.orm import relationship
# Line 3
from app.database import Base
# Line 4
from datetime import datetime

# Line 6
class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, index=True)
    animal_type = Column(String)
    birth_year = Column(Integer)
    color = Column(String)
    deleted_at = Column(DateTime, nullable=True)

    owner = relationship("User", back_populates="animals")

    health_records = relationship("HealthRecord", back_populates="animal")


# Line 18  <-- THIS IS THE ERROR LINE
class HealthRecord(Base):
    __tablename__ = "health_records"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id"))
    # Line 25: ✅ FIXED - Changed from 'date' to 'record_date' to match schema
    record_date = Column(Date, default=date.today)  
    temperature = Column(Float)
    appetite = Column(String)
    milk_yield = Column(Float)
    notes = Column(Text, nullable=True)

    animal = relationship("Animal", back_populates="health_records")

# app/models.py

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(Date, default=date.today)

    # Relationship: A User has many Animals
    animals = relationship("Animal", back_populates="owner")