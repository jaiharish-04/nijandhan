from sqlalchemy.orm import Session
from datetime import datetime
from import models, schemas

def get_weather_record(db: Session, record_id: int):
    return db.query(models.WeatherRecord).filter(models.WeatherRecord.id == record_id).first()

def get_weather_records(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.WeatherRecord).offset(skip).limit(limit).all()

def get_weather_records_by_city(db: Session, city: str):
    return db.query(models.WeatherRecord).filter(models.WeatherRecord.city == city).all()

def get_weather_records_by_date_range(db: Session, start_date: datetime, end_date: datetime):
    return db.query(models.WeatherRecord).filter(
        models.WeatherRecord.date >= start_date,
        models.WeatherRecord.date <= end_date
    ).all()

def get_weather_records_by_city_and_date(db: Session, city: str, date: datetime):
    return db.query(models.WeatherRecord).filter(
        models.WeatherRecord.city == city,
        models.WeatherRecord.date == date
    ).all()

def create_weather_record(db: Session, weather_record: schemas.WeatherRecordCreate):
    db_record = models.WeatherRecord(**weather_record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def update_weather_record(db: Session, record_id: int, weather_record: schemas.WeatherRecordUpdate):
    db_record = db.query(models.WeatherRecord).filter(models.WeatherRecord.id == record_id).first()
    if not db_record:
        return None
    
    update_data = weather_record.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_record, key, value)
    
    db.commit()
    db.refresh(db_record)
    return db_record

def delete_weather_record(db: Session, record_id: int):
    db_record = db.query(models.WeatherRecord).filter(models.WeatherRecord.id == record_id).first()
    if not db_record:
        return False
    
    db.delete(db_record)
    db.commit()
    return True

def get_average_temperature_by_city(db: Session, city: str):
    result = db.query(
        models.WeatherRecord.city,
        db.func.avg(models.WeatherRecord.temperature).label('average_temp')
    ).filter(
        models.WeatherRecord.city == city
    ).group_by(models.WeatherRecord.city).first()
    
    return result

def get_average_humidity_by_city(db: Session, city: str):
    result = db.query(
        models.WeatherRecord.city,
        db.func.avg(models.WeatherRecord.humidity).label('average_humidity')
    ).filter(
        models.WeatherRecord.city == city
    ).group_by(models.WeatherRecord.city).first()
    
    return result