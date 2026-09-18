from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn
import MetaTrader5 as mt5
import redis.asyncio as redis
from pydantic import BaseModel
from typing import Optional

from core.config import settings
from core.security import encrypt_mt5, create_access_token

app = FastAPI(title="MK PRO", version="1.0.0", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis_client: Optional[redis.Redis] = None

class MT5ConnectRequest(BaseModel):
    name: str
    broker: str
    server: str
    login: str
    password: str
    account_type: str = "demo"

@app.on_event("startup")
async def startup():
    global redis_client
    redis_client = await redis.from_url(settings.REDIS_URL, decode_responses=True)
    print("🚀 MK PRO Backend Started - Neon Green Protocol Active")

@app.get("/")
async def root():
    return {
        "system": "MK PRO",
        "status": "ONLINE",
        "mode": "NEON-GREEN",
        "message": "Successfully deployed on Railway. Ready for VPS Engine.",
        "encryption_key_status": "LOADED",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/accounts/connect")
async def connect_account(req: MT5ConnectRequest):
    if not mt5.initialize(login=int(req.login), password=req.password, server=req.server):
        err = mt5.last_error()
        mt5.shutdown()
        raise HTTPException(400, f"MT5 Failed: {err}")
    
    info = mt5.account_info()
    mt5.shutdown()
    
    encrypted = encrypt_mt5(req.password)
    
    return {
        "status": "success",
        "account": req.name,
        "balance": info.balance if info else 0,
        "equity": info.equity if info else 0,
        "encrypted_password": encrypted,
        "message": "MT5 credentials encrypted and verified"
    }

@app.post("/trading/start")
async def start_trading(symbol: str = "XAUUSD", strategy: str = "Hybrid", risk: float = 1.0):
    if redis_client:
        await redis_client.publish("mkpro:commands", 
            f'{{"command":"START","symbol":"{symbol}","strategy":"{strategy}","risk":{risk}}}')
    return {"status": "START command sent to Windows VPS Engine"}

@app.post("/trading/stop")
async def stop_trading():
    if redis_client:
        await redis_client.publish("mkpro:commands", '{"command":"STOP"}')
    return {"status": "STOP command sent"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
