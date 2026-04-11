# 1. اختيار الصورة الأساسية (Python)
FROM python:3.10-slim

# 2. تحديد مجلد العمل داخل السيرفر
WORKDIR /app

# 3. تثبيت المكتبات اللازمة
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. نسخ أكواد المشروع
COPY . .

# 5. تشغيل السيرفر باستخدام Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
