from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.db import create_db_and_tables
from app.routes import auth, tasks, ai

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# 1. إعداد الـ CORS (للسماح لتطبيق الأندرويد بالاتصال)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. إنشاء الجداول عند البداية
@app.on_event("startup")
def on_startup():
    try:
        print("🚀 Starting database initialization...")
        create_db_and_tables()
        print("✅ Database initialized successfully!")
    except Exception as e:
        print("❌ FATAL: Database initialization failed!")
        import traceback
        traceback.print_exc()
        # لا نغلق التطبيق هنا لنسمح للـ Logs بالظهور بوضوح

# 3. ربط المسارات (Routes)
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(tasks.router, prefix=settings.API_V1_STR)
app.include_router(ai.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Welcome to AI Tracking API!", "status": "running"}
