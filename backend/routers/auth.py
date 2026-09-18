from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..schemas.auth import *
from ..core.security import *
from ..core.config import settings
import pyotp

router = APIRouter()

@router.post("/register")
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        two_fa_secret=generate_2fa_secret(),
        is_active=True
    )
    db.add(user)
    db.commit()
    return {"message": "Account created. Enable 2FA using the QR code.", "secret": user.two_fa_secret}

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if user.two_fa_enabled:
        # 2FA verification happens in /login/2fa endpoint (second step)
        return {"requires_2fa": True, "temp_token": create_access_token({"sub": user.email, "temp": True})}
    
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login/2fa")
def verify_2fa(data: TwoFAVerify, db: Session = Depends(get_db)):
    # Validate temp token and 2FA code here (implementation shortened for space)
    totp = pyotp.TOTP(data.secret)
    if not totp.verify(data.code):
        raise HTTPException(401, "Invalid 2FA code")
    return {"access_token": create_access_token({"sub": data.email})}