from pydantic import BaseModel
from datetime import date
from typing import Optional, List

# --- Animal Schemas ---
class AnimalBase(BaseModel):
    name: str
    animal_type: str
    birth_year: int
    color: str

class AnimalCreate(AnimalBase):
    pass  # Inherits all fields from AnimalBase

class AnimalResponse(AnimalBase):
    id: int
    # Optional: Nest the health records inside the animal response
    health_records: List["HealthRecordResponse"] = []

    class Config:
        from_attributes = True  # Enables ORM conversion (SQLAlchemy -> Pydantic)


# --- Health Record Schemas ---
class HealthRecordBase(BaseModel):
    animal_id: int
    date: Optional[date] = date.today()
    temperature: float
    appetite: str  # 'Good', 'Low', 'None'
    milk_yield: float
    notes: Optional[str] = None

class HealthRecordCreate(HealthRecordBase):
    pass

class HealthRecordResponse(HealthRecordBase):
    id: int

    class Config:
        from_attributes = True


# --- Alert Schema (For our custom health warning) ---
class HealthAlertResponse(BaseModel):
    animal_id: int
    animal_name: str
    temperature: float
    milk_yield: float
    warning: str  # e.g., "Fever detected!" or "Low milk production"