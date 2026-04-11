# 1. اختيار الصورة الأساسية (Python)
FROM python:3.10-slim

# 2. تثبيت أدوات النظام اللازمة لـ Postgres
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 3. تحديد مجلد العمل داخل السيرفر
WORKDIR /app

# 4. تثبيت المكتبات اللازمة
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. نسخ أكواد المشروع
COPY . .

# 6. تشغيل السيرفر باستخدام Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
