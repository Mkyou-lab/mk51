from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
import uvicorn
from datetime import datetime
import redis.asyncio as redis

from .core.config import settings
from .core.security import encrypt_mt5_credentials
from .routers import auth, mt5_accounts, trading, dashboard, notifications

app = FastAPI(
    title="MK PRO API",
    description="MK PRO - Professional Forex Trading System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis for real-time communication with VPS engines
redis_client = None

@app.on_event("startup")
async def startup():
    global redis_client
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    print("🚀 MK PRO Backend Started - Neon Green Protocol Active")

@app.get("/")
async def root():
    return {
        "system": "MK PRO",
        "status": "ONLINE",
        "mode": "NEON-GREEN",
        "timestamp": datetime.utcnow().isoformat(),
        "message": "The Future of Trading Has Arrived"
    }

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(mt5_accounts.router, prefix="/accounts", tags=["MT5 Accounts"])
app.include_router(trading.router, prefix="/trading", tags=["Trading"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)