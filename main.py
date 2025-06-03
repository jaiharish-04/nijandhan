from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List
import models
import schemas
import crud
from database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/records/", response_model=schemas.WeatherRecord, status_code=status.HTTP_201_CREATED)
def create_record(record: schemas.WeatherRecordCreate, db: Session = Depends(get_db)):
    return crud.create_weather_record(db=db, weather_record=record)

@app.get("/records/", response_model=List[schemas.WeatherRecord])
def read_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_weather_records(db, skip=skip, limit=limit)

# ... (keep all other endpoints the same as in previous version)

@app.get("/records/{record_id}", response_model=schemas.WeatherRecord)
def read_record(record_id: int, db: Session = Depends(get_db)):
    db_record = crud.get_weather_record(db, record_id=record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return db_record

@app.get("/records/city/{city}", response_model=List[schemas.WeatherRecord])
def read_records_by_city(city: str, db: Session = Depends(get_db)):
    records = crud.get_weather_records_by_city(db, city=city)
    if not records:
        raise HTTPException(status_code=404, detail="No records found for this city")
    return records

@app.get("/records/date/{date}", response_model=List[schemas.WeatherRecord])
def read_records_by_date(date: datetime, db: Session = Depends(get_db)):
    records = crud.get_weather_records_by_date_range(db, start_date=date, end_date=date)
    if not records:
        raise HTTPException(status_code=404, detail="No records found for this date")
    return records

@app.get("/records/city/{city}/date/{date}", response_model=List[schemas.WeatherRecord])
def read_records_by_city_and_date(city: str, date: datetime, db: Session = Depends(get_db)):
    records = crud.get_weather_records_by_city_and_date(db, city=city, date=date)
    if not records:
        raise HTTPException(
            status_code=404,
            detail=f"No records found for city {city} on date {date}"
        )
    return records

@app.put("/records/{record_id}", response_model=schemas.WeatherRecord)
def update_record(
    record_id: int,
    record: schemas.WeatherRecordUpdate,
    db: Session = Depends(get_db)
):
    db_record = crud.update_weather_record(db, record_id=record_id, weather_record=record)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return db_record

@app.delete("/records/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(record_id: int, db: Session = Depends(get_db)):
    success = crud.delete_weather_record(db, record_id=record_id)
    if not success:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"ok": True}

@app.get("/records/city/{city}/average/temperature", response_model=dict)
def get_average_temperature(city: str, db: Session = Depends(get_db)):
    result = crud.get_average_temperature_by_city(db, city=city)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"No records found for city {city} or city does not exist"
        )
    return {"city": result.city, "average_temperature": result.average_temp}

@app.get("/records/city/{city}/average/humidity", response_model=dict)
def get_average_humidity(city: str, db: Session = Depends(get_db)):
    result = crud.get_average_humidity_by_city(db, city=city)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"No records found for city {city} or city does not exist"
        )
    return {"city": result.city, "average_humidity": result.average_humidity}