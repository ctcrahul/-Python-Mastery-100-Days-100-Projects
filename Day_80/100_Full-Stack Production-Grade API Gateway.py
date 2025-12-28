from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
import time
import redis
import hashlib

app = FastAPI()
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

RATE_LIMIT = 5       # requests
WINDOW = 10          # seconds
# ---------------------------
# AUTH SYSTEM
# ---------------------------
API_KEYS = {
    "admin-key-123": "admin",
    "user-key-456": "user"
}

def authenticate(request: Request):
    api_key = request.headers.get("x-api-key")
    if not api_key or api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return API_KEYS[api_key]
# ---------------------------
# RATE LIMITER
# ---------------------------
def rate_limiter(identifier: str):
    key = f"rate:{identifier}"
    now = int(time.time())

    pipe = r.pipeline()
    pipe.zremrangebyscore(key, 0, now - WINDOW)
    pipe.zadd(key, {now: now})
    pipe.zcard(key)
    pipe.expire(key, WINDOW)
    _, _, count, _ = pipe.execute()

    if count > RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
# ---------------------------
# MIDDLEWARE
# ---------------------------
@app.middleware("http")
async def middleware(request: Request, call_next):
    client_ip = request.client.host
    rate_limiter(client_ip)
    response = await call_next(request)
    return response
