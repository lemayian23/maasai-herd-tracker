# Line 1
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text
# Line 2
from sqlalchemy.orm import relationship
# Line 3
from app.database import Base
# Line 4
from datetime import date

# Line 6
class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    animal_type = Column(String)
    birth_year = Column(Integer)
    color = Column(String)

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