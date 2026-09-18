from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime
import uvicorn
import MetaTrader5 as mt5
import redis.asyncio as redis
from pydantic import BaseModel
from typing import Optional

from .core.config import settings
from .core.security import encrypt_mt5, decrypt_mt5, create_access_token, hash_password, verify_password

app = FastAPI(
    title="MK PRO",
    description="Professional Forex Trading System - Neon Green Protocol",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Redis for real-time VPS communication
redis_client: Optional[redis.Redis] = None

class MT5ConnectRequest(BaseModel):
    name: str
    broker: str
    server: str
    login: str
    password: str
    account_type: str = "demo"

@app.on_event("startup")
async def startup_event():
    global redis_client
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    print("🚀 MK PRO Backend Started - Neon Green Protocol Active")

@app.get("/")
async def root():
    return {
        "system": "MK PRO",
        "status": "ONLINE",
        "mode": "NEON-GREEN",
        "message": "Railway deployment successful. Engine ready for VPS connection.",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "mt5_available": mt5.__version__}

@app.post("/accounts/connect")
async def connect_mt5_account(req: MT5ConnectRequest):
    """Test MT5 connection and encrypt credentials"""
    if not mt5.initialize(login=int(req.login), password=req.password, server=req.server):
        error = mt5.last_error()
        mt5.shutdown()
        raise HTTPException(status_code=400, detail=f"MT5 Connection Failed: {error}")

    account_info = mt5.account_info()
    mt5.shutdown()

    encrypted_pass = encrypt_mt5(req.password)

    return {
        "status": "connected",
        "account": {
            "name": req.name,
            "broker": req.broker,
            "server": req.server,
            "login": req.login,
            "account_type": req.account_type,
            "balance": account_info.balance if account_info else 0,
            "equity": account_info.equity if account_info else 0,
            "encrypted_password": encrypted_pass
        },
        "message": "MT5 account verified and credentials encrypted. Ready for engine."
    }

@app.post("/trading/start")
async def start_engine(symbol: str = "XAUUSD", strategy: str = "Hybrid", risk: float = 1.0):
    """Remote command sent to VPS Engine via Redis/WebSocket"""
    if redis_client:
        await redis_client.publish("mkpro-commands", 
            f'{{"command":"START","symbol":"{symbol}","strategy":"{strategy}","risk":{risk}}}')
    return {"status": "command_sent_to_vps", "action": "Engine starting on Windows VPS"}

@app.post("/trading/stop")
async def stop_engine():
    if redis_client:
        await redis_client.publish("mkpro-commands", '{"command":"STOP"}')
    return {"status": "stopped", "message": "Engine stopped. No new trades will open."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
