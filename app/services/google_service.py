import requests
from app.core.config import settings
from app.models.models import User
from sqlmodel import Session
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import json

class GoogleService:
    def __init__(self):
        self.client_id = settings.GOOGLE_CLIENT_ID
        self.client_secret = settings.GOOGLE_CLIENT_SECRET

    async def exchange_auth_code(self, code: str, user: User, db: Session):
        """
        تبادل الـ serverAuthCode القادم من الأندرويد بمفتاح Refresh Token دائم.
        """
        try:
            # إعداد مسار التفويض (OAuth2 Flow)
            flow = Flow.from_client_config(
                {
                    "web": {
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                    }
                },
                scopes=['https://www.googleapis.com/auth/calendar.readonly']
            )
            flow.redirect_uri = 'postmessage' # خاص بالتطبيقات التي تستخدم serverAuthCode
            
            # التبادل الفعلي
            flow.fetch_token(code=code)
            credentials = flow.credentials

            # حفظ الـ Refresh Token في قاعدة البيانات للمستخدم
            user.google_refresh_token = credentials.refresh_token
            db.add(user)
            db.commit()
            
            return True
        except Exception as e:
            print(f"Error exchanging token: {e}")
            return False

    async def get_calendar_events(self, user: User):
        """
        جلب مواعيد التقويم للمستخدم باستخدام الـ Refresh Token المحفوظ.
        """
        if not user.google_refresh_token:
            return []

        creds = Credentials(
            None, # لا نحتاج للـ access token حالياً سيتم تجديده تلقائياً
            refresh_token=user.google_refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=self.client_id,
            client_secret=self.client_secret
        )

        service = build('calendar', 'v3', credentials=creds)
        # جلب المواعيد من الوقت الحالي وحتى 7 أيام قادمة
        events_result = service.events().list(
            calendarId='primary', 
            timeMin=datetime.utcnow().isoformat() + 'Z',
            maxResults=10, 
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        return events_result.get('items', [])

# نسخة وحيدة للعمل بها
google_service = GoogleService()
