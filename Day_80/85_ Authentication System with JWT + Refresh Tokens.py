"""
Project 85 — Authentication System with JWT + Refresh Tokens

Run:
    uvicorn auth_system:app --reload

Routes:
    POST /register
    POST /login
    POST /refresh
    POST /logout
    GET  /protected
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
import bcrypt
import jwt
import uuid

SECRET = "supersecretkey"
REFRESH_SECRET = "refreshsecret"
ACCESS_TTL = 30        # seconds
REFRESH_TTL = 300      # seconds

app = FastAPI()
auth_scheme = HTTPBearer()

users = {}             # username -> {password_hash, refresh_tokens:set}
revoked_refresh_tokens = set()

def hash_pw(pw: str):
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()


def check_pw(pw: str, hashed: str):
    return bcrypt.checkpw(pw.encode(), hashed.encode())


def make_access_token(username):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(seconds=ACCESS_TTL)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")


def make_refresh_token(username):
    token_id = str(uuid.uuid4())
    payload = {
        "sub": username,
        "jti": token_id,
        "exp": datetime.utcnow() + timedelta(seconds=REFRESH_TTL)
    }
    token = jwt.encode(payload, REFRESH_SECRET, algorithm="HS256")
    return token, token_id

