# 1. اختيار الصورة الكاملة لضمان وجود كل مكتبات النظام
FROM python:3.10

# 2. تحديد مجلد العمل
WORKDIR /app

# 3. تثبيت المكتبات
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. نسخ الأكواد
COPY . .

# 5. تشغيل السيرفر
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
