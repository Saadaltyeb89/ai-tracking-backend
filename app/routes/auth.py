from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
import uuid
from app.database.db import get_session
from app.models.models import User
from app.routes.tasks import get_current_user
from app.services.google_service import google_service
from app.core.auth import verify_google_token, create_access_token
from pydantic import BaseModel

# 1. تعريف الـ Router (المفقود سابقاً)
router = APIRouter(prefix="/auth", tags=["Authentication"])

class TokenPayload(BaseModel):
    id_token: str

class GoogleCodeRequest(BaseModel):
    code: str

# 2. استعادة مسار تسجيل الدخول بجوجل
@router.post("/google")
async def google_auth(payload: TokenPayload, db: Session = Depends(get_session)):
    google_data = verify_google_token(payload.id_token)
    email = google_data.get("email")
    name = google_data.get("name")
    google_id = google_data.get("sub")

    if not email:
        raise HTTPException(status_code=400, detail="Email not available in Google account")

    user = db.exec(select(User).where(User.email == email)).first()
    if not user:
        user = User(email=email, full_name=name, google_id=google_id)
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {"id": str(user.id), "email": user.email, "name": user.full_name}
    }

# 3. مسارات تفويض التقويم
@router.post("/google/calendar-auth")
async def exchange_calendar_code(
    payload: GoogleCodeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    success = await google_service.exchange_auth_code(payload.code, current_user, db)
    if not success:
        raise HTTPException(status_code=400, detail="Calendar auth exchange failed")
    return {"status": "success", "message": "Calendar linked successfully"}

@router.get("/google/calendar-events")
async def get_my_calendar(current_user: User = Depends(get_current_user)):
    events = await google_service.get_calendar_events(current_user)
    return {"events": events}
