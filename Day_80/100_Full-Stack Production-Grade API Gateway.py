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
