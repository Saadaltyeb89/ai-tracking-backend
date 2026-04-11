from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.database.db import get_session
from app.models.models import User, Task
from app.routes.tasks import get_current_user
from app.services.ai_service import ai_service
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat_with_assistant(
    request: ChatRequest,
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_session)
):
    """
    دردشة مباشرة مع المساعد الذكي حول المهام والإنتاجية.
    """
    # 1. جلب سياق المهام للمستخدم لتزويد الـ AI به
    tasks = db.exec(select(Task).where(Task.owner_id == current_user.id)).all()
    tasks_str = "\n".join([f"- {t.title} ({'مكتملة' if t.is_completed else 'غير مكتملة'})" for t in tasks])

    # 2. بناء الـ Prompt الخاص بالدردشة
    prompt = f"""
    أنت مساعد شخصي ذكي في تطبيق AI Tracking.
    المستخدم اسمه: {current_user.full_name or "صديقي"}
    قائمة مهامه الحالية:
    {tasks_str}

    سؤال المستخدم هو: "{request.message}"

    أجب عليه بذكاء، ودود، وباللغة العربية (أو العامية السودانية إذا كان السؤال بالعامية).
    ساعده في تنظيم وقته بناءً على مهامه المذكورة أعلاه.
    """

    # 3. الحصول على الرد من Gemini
    response = await ai_service.model.generate_content_async(prompt)
    
    return {"reply": response.text}
