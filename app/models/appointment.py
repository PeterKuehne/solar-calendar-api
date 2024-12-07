from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime, date, time

class AppointmentBase(BaseModel):
    date: str  # Format: YYYY-MM-DD
    time: str  # Format: HH:MM
    email: EmailStr
    name: str
    phone: Optional[str] = None
    notes: Optional[str] = None

    @validator('date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Datum muss im Format YYYY-MM-DD sein (z.B. 2024-12-10)')

    @validator('time')
    def validate_time(cls, v):
        try:
            datetime.strptime(v, '%H:%M')
            return v
        except ValueError:
            raise ValueError('Zeit muss im Format HH:MM sein (z.B. 10:00)')

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentResponse(AppointmentBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
