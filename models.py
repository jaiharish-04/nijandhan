from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base

class WeatherRecord(Base):
    __tablename__ = "weather_records"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True, nullable=False)
    date = Column(DateTime, default=datetime.utcnow, nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    wind_speed = Column(Float, nullable=True)
    description = Column(String, nullable=True)

    def __repr__(self):
        return f"WeatherRecord(city={self.city}, date={self.date}, temperature={self.temperature})"