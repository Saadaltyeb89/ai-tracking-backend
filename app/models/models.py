from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    full_name: Optional[str] = None
    google_id: Optional[str] = Field(unique=True, index=True)
    google_refresh_token: Optional[str] = None # المفتاح السري للمزامنة الدائمة
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    tasks: List["Task"] = Relationship(back_populates="owner")

class Task(SQLModel, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    description: Optional[str] = None
    priority: str = "Medium" # High, Medium, Low
    category: str = "Personal" # Work, Study, Health, Personal
    due_date: Optional[datetime] = None
    is_completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    owner_id: uuid.UUID = Field(foreign_key="user.id")
    owner: User = Relationship(back_populates="tasks")
