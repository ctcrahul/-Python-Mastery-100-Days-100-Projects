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
