from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from app.services.calendar_service import CalendarService
from app.models.appointment import AppointmentCreate, AppointmentResponse

router = APIRouter(
    prefix="/calendar",
    tags=["calendar"],
    responses={404: {"description": "Not found"}},
)

async def get_calendar_service():
    try:
        return CalendarService()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/availability")
async def check_availability(
    datetime: str,
    calendar_service: CalendarService = Depends(get_calendar_service)
) -> Dict[str, Any]:
    """
    Check if a specific time slot is available for booking
    """
    try:
        return await calendar_service.check_availability(datetime)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/appointments", response_model=Dict[str, Any])
async def create_appointment(
    appointment: AppointmentCreate,
    calendar_service: CalendarService = Depends(get_calendar_service)
) -> Dict[str, Any]:
    """
    Create a new appointment
    """
    try:
        return await calendar_service.create_appointment(
            datetime_str=appointment.datetime,
            email=appointment.email,
            name=appointment.name,
            phone=appointment.phone,
            notes=appointment.notes
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/appointments/{appointment_id}")
async def delete_appointment(
    appointment_id: str,
    calendar_service: CalendarService = Depends(get_calendar_service)
) -> Dict[str, Any]:
    """
    Delete an existing appointment
    """
    try:
        return await calendar_service.delete_appointment(appointment_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
