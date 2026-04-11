from sqlmodel import create_engine, SQLModel, Session
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL, 
    echo=True, # سيقوم بطباعة أوامر الـ SQL في الـ Terminal (للمساعدة في التطوير)
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

def create_db_and_tables():
    """
    إنشاء الجداول في قاعدة البيانات عند بداية تشغيل السيرفر.
    """
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    مولد لجلسات قاعدة البيانات (Dependency Injection).
    """
    with Session(engine) as session:
        yield session
