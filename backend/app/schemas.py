# app/schemas.py (FULL CORRECTED VERSION)

from pydantic import BaseModel, Field
from datetime import date, datetime
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
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# --- Health Record Schemas ---
class HealthRecordBase(BaseModel):
    animal_id: int
    record_date: date = Field(default_factory=date.today)
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

# --- User Schemas ---
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    created_at: date

    class Config:
        from_attributes = True

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# --- Profile & Settings Schemas (MISSING - ADD THESE!) ---
class UserUpdateEmail(BaseModel):
    email: str

class UserChangePassword(BaseModel):
    current_password: str
    new_password: str

# --- Pagination Schema ---
class PaginatedAnimalResponse(BaseModel):
    items: List[AnimalResponse]
    total: int
    skip: int
    limit: int

# --- Soft Delete Schemas ---
class AnimalDeleteResponse(BaseModel):
    message: str
    animal_id: int
    deleted_at: datetime

class AnimalRestoreResponse(BaseModel):
    message: str
    animal_id: int