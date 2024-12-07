import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import pytz
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

logger = logging.getLogger(__name__)

class CalendarService:
    def __init__(self):
        """Initialize the Calendar Service with environment variables"""
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        
        # Construct credentials from environment variables
        credentials_info = {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "refresh_token": os.getenv("GOOGLE_REFRESH_TOKEN"),
            "token_uri": "https://oauth2.googleapis.com/token",
        }
        
        try:
            self.credentials = Credentials.from_authorized_user_info(credentials_info)
            self.calendar_id = os.getenv("GOOGLE_CALENDAR_ID")
            self.service = build('calendar', 'v3', credentials=self.credentials)
            self.timezone = pytz.timezone('Europe/Berlin')
            logger.info("Calendar Service successfully initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Calendar Service: {str(e)}")
            raise

    def _validate_datetime(self, date_str: str, time_str: str) -> datetime:
        """Validate and normalize the input date and time strings"""
        try:
            # Kombiniere Datum und Zeit
            datetime_str = f"{date_str}T{time_str}:00"
            dt = datetime.fromisoformat(datetime_str)
            
            # Stelle sicher, dass das Datum in der Zukunft liegt
            now = datetime.now(self.timezone)
            
            # Konvertiere in lokale Zeitzone
            if dt.tzinfo is None:
                dt = self.timezone.localize(dt)
            
            # Wenn das Datum in der Vergangenheit liegt, verschiebe es auf den nächsten möglichen Tag
            if dt < now:
                days_ahead = 1
                while dt < now:
                    dt = dt + timedelta(days=days_ahead)
            
            return dt
        except ValueError as e:
            raise ValueError(f"Ungültiges Datum oder Zeit: {str(e)}")

    async def check_availability(self, date_str: str, time_str: str) -> Dict[str, Any]:
        """Check if a time slot is available"""
        try:
            start_time = self._validate_datetime(date_str, time_str)
            
            # Debug logging
            logger.info(f"Checking availability for: {start_time}")
            logger.info(f"Weekday: {start_time.weekday()}")
            
            # Check business hours (9:00 - 17:00)
            if not (9 <= start_time.hour < 17):
                return {
                    "available": False,
                    "message": "Termine sind nur zwischen 9:00 und 17:00 Uhr möglich."
                }
            
            # Check if it's a workday (0 = Monday, 6 = Sunday)
            if start_time.weekday() >= 5:
                return {
                    "available": False,
                    "message": "Termine sind nur von Montag bis Freitag möglich."
                }

            end_time = start_time + timedelta(minutes=60)
            buffer_start = start_time - timedelta(minutes=30)
            buffer_end = end_time + timedelta(minutes=30)
            
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=buffer_start.isoformat(),
                timeMax=buffer_end.isoformat(),
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            if events:
                return {
                    "available": False,
                    "message": "Dieser Zeitslot ist bereits belegt."
                }
            
            return {
                "available": True,
                "message": "Dieser Zeitslot ist verfügbar."
            }
            
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            logger.error(f"Error checking availability: {str(e)}")
            raise

    async def create_appointment(self,
                               date_str: str,
                               time_str: str,
                               email: str,
                               name: str,
                               phone: Optional[str] = None,
                               notes: Optional[str] = None) -> Dict[str, Any]:
        """Create a new appointment"""
        try:
            # Validate the datetime first
            start_time = self._validate_datetime(date_str, time_str)
            
            # Check availability
            availability = await self.check_availability(date_str, time_str)
            if not availability["available"]:
                raise ValueError(availability["message"])
            
            # Create the event
            end_time = start_time + timedelta(minutes=60)
            
            event = {
                'summary': f'Termin: {name}',
                'description': f'Name: {name}\nEmail: {email}\nTelefon: {phone or "Nicht angegeben"}\nNotizen: {notes or "Keine"}',
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'Europe/Berlin',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'Europe/Berlin',
                },
                'attendees': [
                    {'email': email},
                ],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 30},
                    ],
                },
            }
            
            event = self.service.events().insert(
                calendarId=self.calendar_id,
                body=event,
                sendUpdates='all'
            ).execute()
            
            return {
                "id": event['id'],
                "created": True,
                "message": "Termin wurde erfolgreich gebucht.",
                "details": {
                    "start": start_time.isoformat(),
                    "end": end_time.isoformat(),
                    "name": name,
                    "email": email
                }
            }
            
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            logger.error(f"Error creating appointment: {str(e)}")
            raise

    async def delete_appointment(self, event_id: str) -> Dict[str, Any]:
        """Delete an appointment"""
        try:
            self.service.events().delete(
                calendarId=self.calendar_id,
                eventId=event_id,
                sendUpdates='all'
            ).execute()

            return {
                "deleted": True,
                "id": event_id
            }

        except Exception as e:
            logger.error(f"Error deleting appointment: {str(e)}")
            raise
