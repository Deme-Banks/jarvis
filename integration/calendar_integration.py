"""
Calendar Integration - Google Calendar, Outlook
"""
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class CalendarIntegration:
    """Calendar integration for JARVIS"""
    
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    
    def __init__(self, calendar_type: str = "google"):
        self.calendar_type = calendar_type
        self.service = None
        self._setup_service()
    
    def _setup_service(self):
        """Setup calendar service"""
        if self.calendar_type == "google":
            creds = None
            token_file = "token.json"
            creds_file = "credentials.json"
            
            if os.path.exists(token_file):
                creds = Credentials.from_authorized_user_file(token_file, self.SCOPES)
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(requests.Request())
                else:
                    if os.path.exists(creds_file):
                        flow = InstalledAppFlow.from_client_secrets_file(creds_file, self.SCOPES)
                        creds = flow.run_local_server(port=0)
                
                with open(token_file, 'w') as token:
                    token.write(creds.to_json())
            
            if creds:
                self.service = build('calendar', 'v3', credentials=creds)
    
    def create_event(self, summary: str, start_time: datetime,
                    end_time: Optional[datetime] = None,
                    description: str = "", location: str = "") -> Dict:
        """Create a calendar event"""
        if not self.service:
            return {"error": "Calendar service not configured"}
        
        try:
            if not end_time:
                end_time = start_time + timedelta(hours=1)
            
            event = {
                'summary': summary,
                'description': description,
                'location': location,
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'UTC',
                },
            }
            
            event = self.service.events().insert(calendarId='primary', body=event).execute()
            
            return {
                "success": True,
                "event_id": event['id'],
                "html_link": event.get('htmlLink'),
                "summary": summary
            }
        except HttpError as e:
            return {"error": str(e)}
    
    def list_events(self, max_results: int = 10,
                   time_min: Optional[datetime] = None) -> List[Dict]:
        """List upcoming events"""
        if not self.service:
            return []
        
        try:
            if not time_min:
                time_min = datetime.utcnow()
            
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=time_min.isoformat() + 'Z',
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            return [{
                "summary": event.get('summary'),
                "start": event['start'].get('dateTime', event['start'].get('date')),
                "end": event['end'].get('dateTime', event['end'].get('date')),
                "location": event.get('location', '')
            } for event in events]
        except HttpError as e:
            return [{"error": str(e)}]
    
    def delete_event(self, event_id: str) -> Dict:
        """Delete a calendar event"""
        if not self.service:
            return {"error": "Calendar service not configured"}
        
        try:
            self.service.events().delete(calendarId='primary', eventId=event_id).execute()
            return {"success": True, "event_id": event_id}
        except HttpError as e:
            return {"error": str(e)}
