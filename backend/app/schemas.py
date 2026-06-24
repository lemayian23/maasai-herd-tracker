from pydantic import BaseModel, Field  # <-- ADD Field to this import
from datetime import date
from typing import Optional, List

# --- Animal Schemas ---
class AnimalBase(BaseModel):
    name: str
    animal_type: str
    birth_year: int
    color: str

class AnimalCreate(AnimalBase):
    pass

class AnimalResponse(AnimalBase):
    id: int
    health_records: List["HealthRecordResponse"] = []

    class Config:
        from_attributes = True


# --- Health Record Schemas ---
class HealthRecordBase(BaseModel):
    animal_id: int
    # ✅ FIX: Use default_factory to call date.today() dynamically
    date: date = Field(default_factory=date.today)  
    temperature: float
    appetite: str  
    milk_yield: float
    notes: Optional[str] = None

class HealthRecordCreate(HealthRecordBase):
    pass

class HealthRecordResponse(HealthRecordBase):
    id: int

    class Config:
        from_attributes = True


# --- Alert Schema ---
class HealthAlertResponse(BaseModel):
    animal_id: int
    animal_name: str
    temperature: float
    milk_yield: float
    warning: str