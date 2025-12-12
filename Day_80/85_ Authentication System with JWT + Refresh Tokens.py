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
    # rotate token
    users[username]["refresh_tokens"].remove(jti)
    revoked_refresh_tokens.add(jti)

    new_refresh, new_jti = make_refresh_token(username)
    users[username]["refresh_tokens"].add(new_jti)

    new_access = make_access_token(username)

    return {"access": new_access, "refresh": new_refresh}


@app.post("/logout")
async def logout(request: Request):
    data = await request.json()
    token = data["refresh"]
    payload = verify_refresh_token(token)

    username = payload["sub"]
    jti = payload["jti"]

    if jti in revoked_refresh_tokens:
        return {"status": "already revoked"}

    revoked_refresh_tokens.add(jti)
    users[username]["refresh_tokens"].discard(jti)
    return {"status": "logged out"}



def make_refresh_token(username):
    token_id = str(uuid.uuid4())
    payload = {
        "sub": username,
        "jti": token_id,
        "exp": datetime.utcnow() + timedelta(seconds=REFRESH_TTL)
    }
    token = jwt.encode(payload, REFRESH_SECRET, algorithm="HS256")
    return token, token_id
def verify_access_token(token: str):
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired access token")


def verify_refresh_token(token: str):
    try:
        return jwt.decode(token, REFRESH_SECRET, algorithms=["HS256"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")


@app.post("/register")
async def register(request: Request):
    data = await request.json()
    username = data["username"]
    password = data["password"]

    if username in users:
        raise HTTPException(400, "User exists")

    pw_hash = hash_pw(password)
    users[username] = {"password": pw_hash, "refresh_tokens": set()}
    return {"status": "registered", "user": username}


@app.post("/login")
async def login(request: Request):
    data = await request.json()
    username = data["username"]
    password = data["password"]

    if username not in users:
        raise HTTPException(400, "Unknown user")

    if not check_pw(password, users[username]["password"]):
        raise HTTPException(400, "Wrong password")

    access_token = make_access_token(username)
    refresh_token, token_id = make_refresh_token(username)
    users[username]["refresh_tokens"].add(token_id)

    return {"access": access_token, "refresh": refresh_token}


@app.post("/refresh")
async def refresh(request: Request):
    data = await request.json()
    token = data["refresh"]

    payload = verify_refresh_token(token)
    username = payload["sub"]
    jti = payload["jti"]

    if jti in revoked_refresh_tokens:
        raise HTTPException(401, "Refresh token revoked")

    if jti not in users[username]["refresh_tokens"]:
        raise HTTPException(401, "Refresh token not recognized")
