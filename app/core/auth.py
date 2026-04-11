from datetime import datetime, timedelta
from typing import Optional
from google.oauth2 import id_token
from google.auth.transport import requests
from jose import JWTError, jwt
from fastapi import HTTPException, status
from app.core.config import settings

def verify_google_token(token: str) -> dict:
    """
    التحقق من صحة رمز جوجل المرسل من تطبيق الأندرويد.
    """
    try:
        # التحقق من الرمز باستخدام مكتبة جوجل الرسمية
        idinfo = id_token.verify_oauth2_token(
            token, 
            requests.Request(), 
            settings.GOOGLE_CLIENT_ID
        )

        # التأكد من أن الرمز صادر من جهة موثوقة (جوجل)
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        return idinfo
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"فشل التحقق من رمز جوجل: {str(e)}"
        )

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    إنشاء رمز JWT خاص بتطبيقنا بعد نجاح دخول المستخدم بجوجل.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt
