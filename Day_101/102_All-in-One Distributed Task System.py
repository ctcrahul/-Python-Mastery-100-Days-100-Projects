import time
import threading
import uuid
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import uvicorn

# ---------------- GLOBAL STATE ----------------
TASK_QUEUE = []
TASK_LOG = []
RATE_LIMIT = {}
MAX_REQ = 5
WINDOW = 10  # seconds

# ---------------- UTILS ----------------
def now():
    return int(time.time())

def rate_limit(ip):
    timestamps = RATE_LIMIT.get(ip, [])
    timestamps = [t for t in timestamps if now() - t < WINDOW]

    if len(timestamps) >= MAX_REQ:
        return False

    timestamps.append(now())
    RATE_LIMIT[ip] = timestamps
    return True

