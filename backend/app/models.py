from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import date

class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    animal_type = Column(String)  # e.g., "Cow", "Goat", "Sheep"
    birth_year = Column(Integer)
    color = Column(String)        # e.g., "Black/White"

    # This creates a "virtual" list of health records. 
    # When you fetch an Animal, you can also get its health_records.
    health_records = relationship("HealthRecord", back_populates="animal")


class HealthRecord(Base):
    __tablename__ = "health_records"

    id = Column(Integer, primary_key=True, index=True)
    animal_id = Column(Integer, ForeignKey("animals.id"))
    date = Column(Date, default=date.today)
    temperature = Column(Float)   # Celsius
    appetite = Column(String)     # "Good", "Low", "None"
    milk_yield = Column(Float)    # Liters
    notes = Column(Text, nullable=True)

    # This links back to the Animal
    animal = relationship("Animal", back_populates="health_records")