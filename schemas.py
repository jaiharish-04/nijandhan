from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional

class WeatherRecordBase(BaseModel):
    city: str
    temperature: float
    humidity: float
    wind_speed: Optional[float] = None
    description: Optional[str] = None

    @validator('temperature')
    def temperature_must_be_realistic(cls, v):
        if v < -80 or v > 60:
            raise ValueError('Temperature must be between -80°C and 60°C')
        return v

    @validator('humidity')
    def humidity_must_be_valid(cls, v):
        if v < 0 or v > 100:
            raise ValueError('Humidity must be between 0% and 100%')
        return v

class WeatherRecordCreate(WeatherRecordBase):
    pass

class WeatherRecord(WeatherRecordBase):
    id: int
    date: datetime

    class Config:
        orm_mode = True

class WeatherRecordUpdate(BaseModel):
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    wind_speed: Optional[float] = None
    description: Optional[str] = None

    @validator('temperature')
    def temperature_must_be_realistic(cls, v):
        if v is not None and (v < -80 or v > 60):
            raise ValueError('Temperature must be between -80°C and 60°C')
        return v

    @validator('humidity')
    def humidity_must_be_valid(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError('Humidity must be between 0% and 100%')
        return v