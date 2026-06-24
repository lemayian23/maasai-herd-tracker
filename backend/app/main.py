# Line 1
from fastapi import FastAPI, Depends, HTTPException, status
# Line 2
from fastapi.middleware.cors import CORSMiddleware
# Line 3
from sqlalchemy.orm import Session
# Line 4
from typing import List
# Line 5
from datetime import date

# Line 7
from app.database import engine, get_db
# Line 8
from app import models, schemas

# Line 10
models.Base.metadata.create_all(bind=engine)

# Line 12
app = FastAPI(
    title="Enkang Livestock Health Tracker API",
    description="Backend API for Maasai herders to track cattle health offline.",
    version="1.0.0"
)

# Line 18
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ENDPOINTS ---

# Line 27
@app.get("/")
def read_root():
    return {"message": "Welcome to the Enkang Livestock Tracker API. Visit /docs for Swagger UI."}

# Line 31
@app.post("/api/animals", response_model=schemas.AnimalResponse, status_code=status.HTTP_201_CREATED)
def create_animal(animal: schemas.AnimalCreate, db: Session = Depends(get_db)):
    db_animal = models.Animal(**animal.dict())
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal

# Line 40
@app.get("/api/animals", response_model=List[schemas.AnimalResponse])
def get_all_animals(db: Session = Depends(get_db)):
    animals = db.query(models.Animal).all()
    return animals

# Line 46
@app.get("/api/animals/{animal_id}", response_model=schemas.AnimalResponse)
def get_animal(animal_id: int, db: Session = Depends(get_db)):
    animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal

# Line 54
@app.post("/api/records", response_model=schemas.HealthRecordResponse, status_code=status.HTTP_201_CREATED)
def create_health_record(record: schemas.HealthRecordCreate, db: Session = Depends(get_db)):
    animal = db.query(models.Animal).filter(models.Animal.id == record.animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    
    db_record = models.HealthRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

# Line 67  <-- THIS IS THE ERROR SECTION
@app.get("/api/alerts", response_model=List[schemas.HealthAlertResponse])
def get_health_alerts(db: Session = Depends(get_db)):
    alerts = []
    animals = db.query(models.Animal).all()
    
    for animal in animals:
        latest_record = db.query(models.HealthRecord).filter(
            models.HealthRecord.animal_id == animal.id
        ).order_by(models.HealthRecord.record_date.desc()).first()  # ✅ FIXED: Changed 'date' to 'record_date'
        
        if latest_record:
            warning = None
            # Line 78: ✅ FIXED: Changed 'date' to 'record_date'
            if latest_record.temperature > 39.5:
                warning = "🔥 Fever detected! Temperature above 39.5°C"
            # Line 80: ✅ FIXED: Changed 'date' to 'record_date'
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