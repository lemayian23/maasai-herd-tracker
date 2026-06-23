from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from app.database import engine, get_db
from app import models, schemas

# Create the database tables automatically (if they don't exist)
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
    title="Enkang Livestock Health Tracker API",
    description="Backend API for Maasai herders to track cattle health offline.",
    version="1.0.0"
)

# Enable CORS so your future HTML/JS frontend can talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ENDPOINTS ---

@app.get("/")
def read_root():
    return {"message": "Welcome to the Enkang Livestock Tracker API. Visit /docs for Swagger UI."}

# 1. CREATE a new animal
@app.post("/api/animals", response_model=schemas.AnimalResponse, status_code=status.HTTP_201_CREATED)
def create_animal(animal: schemas.AnimalCreate, db: Session = Depends(get_db)):
    db_animal = models.Animal(**animal.dict())
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal

# 2. GET all animals
@app.get("/api/animals", response_model=List[schemas.AnimalResponse])
def get_all_animals(db: Session = Depends(get_db)):
    animals = db.query(models.Animal).all()
    return animals

# 3. GET a single animal by ID (includes its health records)
@app.get("/api/animals/{animal_id}", response_model=schemas.AnimalResponse)
def get_animal(animal_id: int, db: Session = Depends(get_db)):
    animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal

# 4. CREATE a health record for an animal
@app.post("/api/records", response_model=schemas.HealthRecordResponse, status_code=status.HTTP_201_CREATED)
def create_health_record(record: schemas.HealthRecordCreate, db: Session = Depends(get_db)):
    # Check if the animal exists first
    animal = db.query(models.Animal).filter(models.Animal.id == record.animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    
    db_record = models.HealthRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

# 5. GET health alerts (Livestock with potential issues)
@app.get("/api/alerts", response_model=List[schemas.HealthAlertResponse])
def get_health_alerts(db: Session = Depends(get_db)):
    alerts = []
    # Query the latest health record for every animal (using a subquery)
    # For simplicity (and to avoid complex SQL for beginners), we fetch all animals 
    # and check their most recent record in Python. 
    animals = db.query(models.Animal).all()
    
    for animal in animals:
        # Get the most recent record for this animal
        latest_record = db.query(models.HealthRecord).filter(
            models.HealthRecord.animal_id == animal.id
        ).order_by(models.HealthRecord.date.desc()).first()
        
        if latest_record:
            warning = None
            # Alert logic
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