from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List

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

class HealthRecordBase(BaseModel):
    animal_id: int
    date: date = Field(default_factory=date.today)  # This is correct
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

class HealthAlertResponse(BaseModel):
    animal_id: int
    animal_name: str
    temperature: float
    milk_yield: float
    warning: str