# Line 1
from pydantic import BaseModel, Field
# Line 2
from datetime import date
# Line 3
from typing import Optional, List

# --- Animal Schemas ---
# Line 6
class AnimalBase(BaseModel):
    name: str
    animal_type: str
    birth_year: int
    color: str

# Line 12
class AnimalCreate(AnimalBase):
    pass

# Line 15
class AnimalResponse(AnimalBase):
    id: int
    health_records: List["HealthRecordResponse"] = []

    class Config:
        from_attributes = True


# --- Health Record Schemas ---
# Line 24  <-- THIS IS THE ERROR LINE
class HealthRecordBase(BaseModel):
    animal_id: int
    # Line 27: ✅ FIXED - Renamed 'date' to 'record_date' to avoid clash
    record_date: date = Field(default_factory=date.today)  
    temperature: float
    appetite: str  
    milk_yield: float
    notes: Optional[str] = None

# Line 34
class HealthRecordCreate(HealthRecordBase):
    pass

# Line 37
class HealthRecordResponse(HealthRecordBase):
    id: int

    class Config:
        from_attributes = True


# --- Alert Schema ---
# Line 45
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


# --- Profile & Settings Schemas ---
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