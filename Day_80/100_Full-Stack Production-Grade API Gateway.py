from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
import time
import redis
import hashlib

app = FastAPI()
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

RATE_LIMIT = 5       # requests
WINDOW = 10          # seconds
