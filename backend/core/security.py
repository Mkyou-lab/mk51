from cryptography.fernet import Fernet
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
fernet = Fernet(settings.ENCRYPTION_KEY.encode())

def encrypt_mt5(password: str) -> str:
    return fernet.encrypt(password.encode()).decode()

def decrypt_mt5(encrypted: str) -> str:
    return fernet.decrypt(encrypted.encode()).decode()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=1)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm="HS256")
