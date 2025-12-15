"""
Project 87 — URL Shortener (Flask + SQLite)

Routes:
POST /shorten   { "url": "https://example.com" }
GET  /<code>    -> redirect
GET  /stats/<code>
"""

import sqlite3
import string
import random
from flask import Flask, request, redirect, jsonify

DB = "urls.db"
BASE62 = string.ascii_letters + string.digits

app = Flask(__name__)


def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                code TEXT PRIMARY KEY,
                url TEXT NOT NULL,
                clicks INTEGER DEFAULT 0
            )
        """)
