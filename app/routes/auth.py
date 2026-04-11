from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database.db import get_session
from app.models.models import User
from app.routes.tasks import get_current_user
from app.services.google_service import google_service
from pydantic import BaseModel

class GoogleCodeRequest(BaseModel):
    code: str

@router.post("/google/calendar-auth")
async def exchange_calendar_code(
    payload: GoogleCodeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """
    استقبال رمز الـ Server Auth Code وتبادله بمفتاح Refresh Token دائم.
    """
    success = await google_service.exchange_auth_code(payload.code, current_user, db)
    if not success:
        raise HTTPException(status_code=400, detail="فشل تبادل رمز التقويم")
    
    return {"status": "success", "message": "تم ربط التقويم بنجاح"}

@router.get("/google/calendar-events")
async def get_my_calendar(
    current_user: User = Depends(get_current_user)
):
    """
    جلب مواعيد التقويم الحالية للمستخدم.
    """
    events = await google_service.get_calendar_events(current_user)
    return {"events": events}
