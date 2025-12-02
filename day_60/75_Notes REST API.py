"""
Project 75 — Notes REST API
Run: python notes_api.py
Requirements: Python 3.8+, Flask
Install: pip install Flask

Features:
- Create, read, update, delete notes
- Search notes by text
- Pagination (page, per_page)
- Export notes as CSV
- Minimal validation and clear JSON responses
"""

from flask import Flask, request, jsonify, g, send_file, abort
import sqlite3
from datetime import datetime
import csv
import io
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "notes.db")
APP = Flask(__name__)


# ---------- Database helpers ----------
def get_db():
    db = getattr(g, "_db", None)
    if db is None:
        db = g._db = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db
