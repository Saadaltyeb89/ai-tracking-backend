from sqlmodel import create_engine, SQLModel, Session
from app.core.config import settings

# تصحيح رابط قاعدة البيانات ليتوافق مع SQLAlchemy 2.0 والمحرك المتوفر (Psycopg 3)
database_url = settings.DATABASE_URL
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
elif database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(
    database_url, 
    echo=True, 
    connect_args={"check_same_thread": False} if "sqlite" in database_url else {}
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
