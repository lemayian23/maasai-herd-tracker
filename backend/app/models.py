# app/models.py (FULL CORRECTED VERSION)

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text, DateTime  # <-- Added Date & DateTime here
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import date  # <-- For date.today default

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(Date, default=date.today)

    animals = relationship("Animal", back_populates="owner")


class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, index=True)
    animal_type = Column(String)
    birth_year = Column(Integer)
    color = Column(String)
    deleted_at = Column(DateTime, nullable=True)  # <-- Soft delete column

    owner = relationship("User", back_populates="animals")
    health_records = relationship("HealthRecord", back_populates="animal")


class HealthRecord(Base):
    __tablename__ = "health_records"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id"))
    record_date = Column(Date, default=date.today)  # <-- This is what was failing
    temperature = Column(Float)
    appetite = Column(String)
    milk_yield = Column(Float)
    notes = Column(Text, nullable=True)

    animal = relationship("Animal", back_populates="health_records")