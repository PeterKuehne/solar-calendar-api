from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class AppointmentBase(BaseModel):
    datetime: str
    email: EmailStr
    name: str
    phone: Optional[str] = None
    notes: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentResponse(AppointmentBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
