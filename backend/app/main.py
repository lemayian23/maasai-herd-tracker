# app/main.py (Full rewrite with Auth)

from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import date, timedelta

from app.database import engine, get_db
from app import models, schemas, auth

# Create tables (including the new User table)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Enkang Tracker with Auth", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROOT ---
@app.get("/")
def read_root():
    return {"message": "Welcome to Enkang Tracker. Please login."}

# --- AUTH ENDPOINTS ---

@app.post("/api/register", response_model=schemas.UserResponse, status_code=201)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if username exists
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Hash the password and save
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/api/login", response_model=schemas.Token)
def login(user_login: schemas.UserLogin, db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, user_login.username, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- PROTECTED ANIMAL ENDPOINTS ---
# Notice the "current_user" dependency. If the token is invalid, it rejects the request.

@app.post("/api/animals", response_model=schemas.AnimalResponse, status_code=201)
def create_animal(
    animal: schemas.AnimalCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)  # <-- PROTECTED
):
    # The animal is automatically owned by the logged-in user
    db_animal = models.Animal(**animal.dict(), owner_id=current_user.id)
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal

# app/main.py (Replace the GET /api/animals endpoint)

from typing import Optional  # Ensure this is imported at the top

@app.get("/api/animals", response_model=schemas.PaginatedAnimalResponse)
def get_all_animals(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Get all animals for the current user with pagination and search.
    - skip: number of records to skip (default 0)
    - limit: max records to return (default 10)
    - search: optional search term for animal name (case-insensitive)
    """
    # Base query: only this user's animals
    query = db.query(models.Animal).filter(models.Animal.owner_id == current_user.id)
    
    # Apply search filter if provided
    if search:
        # ilike is case-insensitive for SQLite/PostgreSQL
        query = query.filter(models.Animal.name.ilike(f"%{search}%"))
    
    # Get total count before pagination
    total = query.count()
    
    # Apply pagination
    items = query.offset(skip).limit(limit).all()
    
    return schemas.PaginatedAnimalResponse(
        items=items,
        total=total,
        skip=skip,
        limit=limit
    )

@app.get("/api/animals/{animal_id}", response_model=schemas.AnimalResponse)
def get_animal(
    animal_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)  # <-- PROTECTED
):
    animal = db.query(models.Animal).filter(
        models.Animal.id == animal_id,
        models.Animal.owner_id == current_user.id  # Ensure they own it
    ).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal

# MUST UPDATE THE HEALTH RECORDS ENDPOINTS TOO!
# I will include the updated version below.

@app.post("/api/records", response_model=schemas.HealthRecordResponse, status_code=201)
def create_health_record(
    record: schemas.HealthRecordCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)  # <-- PROTECTED
):
    # Verify the animal belongs to this user before adding record
    animal = db.query(models.Animal).filter(
        models.Animal.id == record.animal_id,
        models.Animal.owner_id == current_user.id
    ).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found or not owned by you")
    
    db_record = models.HealthRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

# --- USER PROFILE ENDPOINTS ---

@app.get("/api/users/me", response_model=schemas.UserResponse)
def get_current_user_profile(current_user: models.User = Depends(auth.get_current_user)):
    """
    Returns the profile information of the currently logged-in user.
    """
    return current_user

@app.patch("/api/users/me/email", response_model=schemas.UserResponse)
def update_user_email(
    email_update: schemas.UserUpdateEmail,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Updates the logged-in user's email address.
    """
    # Check if the new email is already taken by another user
    existing_user = db.query(models.User).filter(
        models.User.email == email_update.email,
        models.User.id != current_user.id  # Exclude the current user
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already in use by another account.")
    
    current_user.email = email_update.email
    db.commit()
    db.refresh(current_user)
    return current_user

@app.post("/api/users/me/change-password")
def change_password(
    password_data: schemas.UserChangePassword,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """
    Changes the user's password after verifying the current password.
    """
    # 1. Verify the current password
    if not auth.verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect.")
    
    # 2. Hash the new password
    new_hashed_password = auth.get_password_hash(password_data.new_password)
    
    # 3. Update the user
    current_user.hashed_password = new_hashed_password
    db.commit()
    
    return {"message": "Password updated successfully."}

@app.get("/api/alerts", response_model=List[schemas.HealthAlertResponse])
def get_health_alerts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)  # <-- PROTECTED
):
    alerts = []
    # Only fetch animals for this user
    animals = db.query(models.Animal).filter(models.Animal.owner_id == current_user.id).all()
    
    for animal in animals:
        latest_record = db.query(models.HealthRecord).filter(
            models.HealthRecord.animal_id == animal.id
        ).order_by(models.HealthRecord.record_date.desc()).first()
        
        if latest_record:
            warning = None
            if latest_record.temperature > 39.5:
                warning = "🔥 Fever detected! Temperature above 39.5°C"
            elif latest_record.milk_yield < 5 and latest_record.appetite == "Low":
                warning = "⚠️ Low milk yield and poor appetite. Check for infection."
            
            if warning:
                alerts.append({
                    "animal_id": animal.id,
                    "animal_name": animal.name,
                    "temperature": latest_record.temperature,
                    "milk_yield": latest_record.milk_yield,
                    "warning": warning
                })
    return alerts

    