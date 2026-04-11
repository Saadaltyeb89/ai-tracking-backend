from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database.db import get_session
from app.models.models import User, Task
from app.core.config import settings
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
import uuid

router = APIRouter(prefix="/tasks", tags=["Tasks"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/google")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)) -> User:
    """
    بالتأكد من هوية المستخدم عبر الـ Token قبل السماح له بالوصول للمهام.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token غير صالح")
    except JWTError:
        raise HTTPException(status_code=401, detail="فشل التحقق من الهوية")
    
    user = db.get(User, uuid.UUID(user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
    return user

@router.post("/", response_model=Task)
async def create_task(task_data: Task, current_user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    task_data.owner_id = current_user.id
    db.add(task_data)
    db.commit()
    db.refresh(task_data)
    return task_data

@router.get("/", response_model=List[Task])
async def list_tasks(current_user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    tasks = db.exec(select(Task).where(Task.owner_id == current_user.id)).all()
    return tasks

@router.patch("/{task_id}/complete")
async def toggle_task_status(task_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    task = db.get(Task, task_id)
    if not task or task.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="المهمة غير موجودة")
    
    task.is_completed = not task.is_completed
    db.add(task)
    db.commit()
    db.refresh(task)
    return task
