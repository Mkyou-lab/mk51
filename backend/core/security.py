from cryptography.fernet import Fernet
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from .config import settings
import pyotp

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
fernet = Fernet(settings.ENCRYPTION_KEY.encode())

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def encrypt_mt5(password: str) -> str:
    return fernet.encrypt(password.encode()).decode()

def decrypt_mt5(encrypted: str) -> str:
    return fernet.decrypt(encrypted.encode()).decode()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm="HS256")

def generate_2fa_secret() -> str:
    return pyotp.random_base32()

def get_2fa_uri(secret: str, email: str) -> str:
    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(name=email, issuer_name="MK PRO")